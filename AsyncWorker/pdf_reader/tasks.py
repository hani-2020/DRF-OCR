from .models import ExtractionJob, ExtractedText, PDFDocument
from celery import shared_task
from elasticsearch import Elasticsearch
from pdf2image import convert_from_path
from django.conf import settings
from PIL import Image
import pytesseract
import os
import cv2


es = Elasticsearch(hosts=["http://elastic-search:9200"])

def start_pdf_extraction(pdf_document, job):
    temp_dir = os.path.join(settings.BASE_DIR, "temp_images")
    os.makedirs(temp_dir, exist_ok=True)
    pages = convert_from_path(pdf_document.file_path.path)
    for i, page_image in enumerate(pages):
        tmp_path = f"{temp_dir}/{pdf_document.id}_page_{i+1}.png"
        page_image.save(tmp_path, "PNG")
        ocr_page.delay(pdf_document.id, i+1, tmp_path, job.id, len(pages))

@shared_task(bind=True)
def start_pdf_extraction_task(self, pdf_document_id, job_id):
    pdf_document = PDFDocument.objects.get(id=pdf_document_id)
    job = ExtractionJob.objects.get(id=job_id)
    start_pdf_extraction(pdf_document, job)

@shared_task(bind=True)
def ocr_page(self, document_id, page_number, page_image_path, job_id, total_pages):
    try:
        img = cv2.imread(page_image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bw = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        preprocessed_path = page_image_path.replace(".png", "_bw.png")
        cv2.imwrite(preprocessed_path, bw)
        text = pytesseract.image_to_string(preprocessed_path)
        layout = {}
        ExtractedText.objects.create(
            document_id=document_id,
            page_number=page_number,
            text=text,
            layout=layout
        )
        es.index(
            index="pdf_pages",
            id=f"{document_id}_{page_number}",
            document={"document_id": document_id, "page_number": page_number, "text": text}
        )
        job = ExtractionJob.objects.get(id=job_id)
        job.progress = (page_number//total_pages) * 100
        job.save()
        os.remove(page_image_path)
        if page_number == total_pages:
            job.status = "COMPLETED"
            job.save()
            pdf_document = job.document
            os.remove(pdf_document.file_path.path)
        return page_number
    except Exception as e:
        job = ExtractionJob.objects.get(id=job_id)
        job.last_error = str(e)
        job.attempts += 1
        job.save()
        raise e