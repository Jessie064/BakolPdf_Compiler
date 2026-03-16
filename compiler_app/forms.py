from django import forms
from django.forms.widgets import FileInput


MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB


class MultipleFileInput(FileInput):
    """FileInput widget that supports multiple file selection."""
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """FileField that returns a list of files rather than a single file."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'accept': '.pdf'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # data is already a list from the widget
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class MultiPDFUploadForm(forms.Form):
    files = MultipleFileField(label='PDF Files')

    def clean_files(self):
        # cleaned_data['files'] is a list of InMemoryUploadedFile objects
        uploaded = self.cleaned_data.get('files', [])
        if not uploaded:
            raise forms.ValidationError("Please select at least one PDF file.")

        cleaned = []
        for f in uploaded:
            # Extension check
            if not f.name.lower().endswith('.pdf'):
                raise forms.ValidationError(
                    f'"{f.name}" is not a PDF file. Only .pdf files are accepted.'
                )
            # Content-type check
            ct = getattr(f, 'content_type', '')
            if ct and ct not in ('application/pdf', 'application/x-pdf'):
                raise forms.ValidationError(
                    f'"{f.name}" does not appear to be a valid PDF.'
                )
            # Size check
            if f.size > MAX_FILE_SIZE:
                size_mb = f.size / (1024 * 1024)
                raise forms.ValidationError(
                    f'"{f.name}" is {size_mb:.1f} MB, which exceeds the 20 MB limit.'
                )
            cleaned.append(f)

        return cleaned
