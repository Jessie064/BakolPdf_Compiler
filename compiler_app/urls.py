from django.urls import path
from . import views

app_name = 'compiler_app'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('arrange/', views.arrange_view, name='arrange'),
    path('compile/', views.compile_view, name='compile'),
    path('download/', views.download_view, name='download'),
    path('delete/<int:pk>/', views.delete_file_view, name='delete_file'),
    path('clear/', views.clear_session_view, name='clear_session'),
]
