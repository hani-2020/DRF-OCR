from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PDFDocument, ExtractionJob
from .serializers import UploadPDFSerializer, PDFDocumentSerializer, JobSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from .tasks import start_pdf_extraction_task
from django.http import StreamingHttpResponse
from elasticsearch import Elasticsearch
import time
import json

es = Elasticsearch(hosts=["http://elastic-search:9200"])

class UploadPDF(APIView):
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = UploadPDFSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            pdf_document = PDFDocument.objects.create(file_path=file, title=file.name)
            job = ExtractionJob.objects.create(document=pdf_document, status='PENDING')
            start_pdf_extraction_task.delay(pdf_document.id, job.id)
            response = {
                "job_id": job.id,
                "data": serializer.data
            }
            return Response(response, status=200)
        return Response(serializer.errors, status=400)

class GetExtractionJob(APIView):
    def get(self, request, job_id):
        def event_stream():
            while True:
                try:
                    job = ExtractionJob.objects.get(id=job_id)
                except ExtractionJob.DoesNotExist:
                    yield "data: {\"error\": \"Job not found\"}\n\n"
                    break
                data = json.dumps({
                    "id": job.id,
                    "status": job.status,
                    "progress": job.progress,
                    "last_error": job.last_error
                })
                yield f"data: {data}\n\n"
                if job.status in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(1)

        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response

class GetFiles(APIView):
    def get(self, request):
        files = PDFDocument.objects.all()
        serializer = PDFDocumentSerializer(files, many=True)
        return Response(serializer.data, status=200)

class GetFile(APIView):
    def get(self, request, file_id):
        file = PDFDocument.objects.get(id=file_id)
        serializer = PDFDocumentSerializer(file)
        return Response(serializer.data, status=200)

class GetExtractionJobs(APIView):
    def get(self, request):
        jobs = ExtractionJob.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=200)

class SearchText(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)
        search_body = {
            "query": {
                "match_phrase_prefix": {
                    "text": query
                }
            }
        }
        try:
            results = es.search(index="pdf_pages", body=search_body)
            hits = results['hits']['hits']
            formatted_results = []
            for hit in hits:
                formatted_results.append({
                    "document_id": hit['_source']['document_id'],
                    "page_number": hit['_source']['page_number'],
                    "text": hit['_source']['text'],
                    "score": hit['_score']
                })     
            return Response(formatted_results, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
