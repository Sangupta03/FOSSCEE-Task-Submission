from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Dataset
from .serializers import DatasetSerializer
from .utils import analyze_csv
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def upload_csv(request):
    """
    POST /api/upload/
    Body: form-data -> key: file, value: CSV file
    """
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        summary = analyze_csv(file)
    except Exception as e:
        return Response(
            {"error": f"CSV processing failed: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔥 NEW: Health Score
    alerts = summary.get("alerts", [])
    health_score = max(0, 100 - (len(alerts) * 10))
    summary["health_score"] = health_score

    Dataset.objects.create(
        filename=file.name,
        summary=summary
    )

    # keep only last 5 uploads (delete older)
    datasets = Dataset.objects.order_by('-uploaded_at')
    if datasets.count() > 5:
        for old in datasets[5:]:
            old.delete()

    return Response(
        {"message": "File uploaded successfully", "summary": summary},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
def latest_summary(request):
    """
    GET /api/summary/
    Returns summary of latest uploaded dataset
    """
    dataset = Dataset.objects.order_by('-uploaded_at').first()

    if not dataset:
        return Response({"message": "No data available"}, status=status.HTTP_200_OK)

    return Response(dataset.summary, status=status.HTTP_200_OK)



@api_view(['GET'])
def history(request):
    datasets = Dataset.objects.order_by('-uploaded_at')[:5]
    serializer = DatasetSerializer(datasets, many=True)

    # Trend detection
    health_scores = [
        d.summary.get("health_score", 0) for d in datasets
    ]

    trend = "Stable"
    if len(health_scores) >= 2:
        if health_scores[0] > health_scores[-1]:
            trend = "Improving"
        elif health_scores[0] < health_scores[-1]:
            trend = "Declining"

    return Response({
        "history": serializer.data,
        "trend": trend
    })



def generate_pdf_report(request):
    latest = Dataset.objects.order_by("-uploaded_at").first()

    if not latest:
        return HttpResponse("No data available", status=404)

    summary = latest.summary

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="equipment_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    y = height - 60
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, y, "Chemical Equipment Report")
    y -= 30

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Dataset: {latest.filename}")
    y -= 20
    p.drawString(50, y, f"Uploaded At: {latest.uploaded_at}")
    y -= 30

    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, y, "Summary")
    y -= 20

    p.setFont("Helvetica", 12)
    for k, v in summary.items():
        p.drawString(50, y, f"{k}: {v}")
        y -= 18
        if y < 80:
            p.showPage()
            y = height - 60

    p.showPage()
    p.save()
    return response
