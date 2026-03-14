from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.UploadPDF.as_view(), name='upload_pdf'),
    path('files/', views.GetFiles.as_view(), name='get_files'),
    path('files/<int:file_id>/', views.GetFile.as_view(), name='get_file'),
    path('files/<int:file_id>/', views.GetFile.as_view(), name='delete_file'),
    path('jobs/', views.GetExtractionJobs.as_view(), name='get_extraction_jobs'),
    path('jobs/<int:job_id>/', views.GetExtractionJob.as_view(), name='get_extraction_job'),
    path('search/', views.SearchText.as_view(), name='search_text'),
]