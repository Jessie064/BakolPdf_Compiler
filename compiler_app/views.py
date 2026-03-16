import json
import os
import uuid

from django.conf import settings
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import MultiPDFUploadForm
from .models import UploadedFile


def _get_or_create_session(request):
    """Ensure the session exists and return its key."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _session_files(request):
    """Return queryset of files for the current session, ordered."""
    sk = _get_or_create_session(request)
    return UploadedFile.objects.filter(session_key=sk).order_by('order', 'id')


# ─── Upload ──────────────────────────────────────────────────────────────────

def upload_view(request):
    form = MultiPDFUploadForm()
    errors = []

    if request.method == 'POST':
        form = MultiPDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sk = _get_or_create_session(request)
            existing_names = set(
                UploadedFile.objects.filter(session_key=sk).values_list('filename', flat=True)
            )
            # Determine starting order
            max_order = UploadedFile.objects.filter(session_key=sk).count()

            for f in form.cleaned_data['files']:
                name = f.name
                # Deduplicate filenames
                if name in existing_names:
                    base, ext = os.path.splitext(name)
                    name = f"{base}_{uuid.uuid4().hex[:6]}{ext}"
                existing_names.add(name)

                uploaded = UploadedFile(
                    filename=name,
                    session_key=sk,
                    order=max_order,
                )
                uploaded.file.save(name, f, save=True)
                max_order += 1

            return redirect('compiler_app:arrange')
        else:
            for field_errors in form.errors.values():
                errors.extend(field_errors)

    files = _session_files(request)
    return render(request, 'compiler_app/upload.html', {
        'form': form,
        'files': files,
        'errors': errors,
    })


# ─── Arrange ─────────────────────────────────────────────────────────────────

def arrange_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            order_list = data.get('order', [])  # list of PKs in desired order
            sk = _get_or_create_session(request)
            for idx, pk in enumerate(order_list):
                UploadedFile.objects.filter(pk=int(pk), session_key=sk).update(order=idx)
            return JsonResponse({'status': 'ok'})
        except (json.JSONDecodeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)

    files = list(_session_files(request))
    if not files:
        return redirect('compiler_app:upload')

    return render(request, 'compiler_app/arrange.html', {'files': files})


# ─── Compile ─────────────────────────────────────────────────────────────────

def compile_view(request):
    if request.method != 'POST':
        return redirect('compiler_app:arrange')

    files = list(_session_files(request))
    if not files:
        return redirect('compiler_app:upload')

    # Save order if provided
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])
        if order_list:
            sk = _get_or_create_session(request)
            for idx, pk in enumerate(order_list):
                UploadedFile.objects.filter(pk=int(pk), session_key=sk).update(order=idx)
            files = list(_session_files(request))
    except (json.JSONDecodeError, ValueError, AttributeError):
        pass
     
    # pyright: ignore[reportMissingImports]
    from pypdf import PdfWriter

    writer = PdfWriter()
    for uf in files:
        file_path = os.path.join(settings.MEDIA_ROOT, uf.file.name)
        if os.path.exists(file_path):
            writer.append(file_path)

    # Save compiled PDF
    compiled_dir = os.path.join(settings.MEDIA_ROOT, 'compiled')
    os.makedirs(compiled_dir, exist_ok=True)

    output_name = f"MergedPDF_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join(compiled_dir, output_name)

    with open(output_path, 'wb') as out_f:
        writer.write(out_f)
    writer.close()

    # Store path in session for download
    request.session['compiled_file'] = f"compiled/{output_name}"
    request.session['compiled_name'] = output_name

    return JsonResponse({'status': 'ok', 'redirect': '/download/'})


# ─── Download ────────────────────────────────────────────────────────────────

def download_view(request):
    compiled_rel = request.session.get('compiled_file')
    compiled_name = request.session.get('compiled_name', 'MergedPDF.pdf')

    if not compiled_rel:
        return redirect('compiler_app:upload')

    output_path = os.path.join(settings.MEDIA_ROOT, compiled_rel)
    if not os.path.exists(output_path):
        return redirect('compiler_app:upload')

    if request.GET.get('dl') == '1':
        with open(output_path, 'rb') as f:
            pdf_data = f.read()
        response = HttpResponse(pdf_data, content_type='application/pdf')
        # Use a safe ASCII filename for the Content-Disposition header
        safe_name = compiled_name.encode('ascii', errors='replace').decode('ascii')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}"'
        return response

    files = list(_session_files(request))
    file_count = len(files)
    return render(request, 'compiler_app/result.html', {
        'compiled_name': compiled_name,
        'file_count': file_count,
    })


# ─── Delete single file ───────────────────────────────────────────────────────

@require_POST
def delete_file_view(request, pk):
    sk = _get_or_create_session(request)
    uf = get_object_or_404(UploadedFile, pk=pk, session_key=sk)
    # Remove physical file
    file_path = os.path.join(settings.MEDIA_ROOT, uf.file.name)
    if os.path.exists(file_path):
        os.remove(file_path)
    uf.delete()
    return JsonResponse({'status': 'ok'})


# ─── Clear all session files ──────────────────────────────────────────────────

@require_POST
def clear_session_view(request):
    sk = _get_or_create_session(request)
    files = UploadedFile.objects.filter(session_key=sk)
    for uf in files:
        file_path = os.path.join(settings.MEDIA_ROOT, uf.file.name)
        if os.path.exists(file_path):
            os.remove(file_path)
    files.delete()
    # Clear compiled session vars
    request.session.pop('compiled_file', None)
    request.session.pop('compiled_name', None)
    return redirect('compiler_app:upload')
