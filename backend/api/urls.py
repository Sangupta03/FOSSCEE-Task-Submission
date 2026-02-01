from django.urls import path
from .views import upload_csv, latest_summary, history, generate_pdf_report

urlpatterns = [
    path('upload/', upload_csv),
    path('summary/', latest_summary),
    path('history/', history),
    path("report/pdf/", generate_pdf_report),
]
