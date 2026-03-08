from django.db import models

class PDFDocument(models.Model):
    title = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ExtractedText(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='extracted_texts')
    page_number = models.IntegerField()
    text = models.TextField()
    layout = models.JSONField()

    def __str__(self):
        return f"Page {self.page_number} of {self.document.title}"

class ExtractionJob(models.Model):
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='extraction_jobs')
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attempts = models.IntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    progress = models.IntegerField(default=0)

    def __str__(self):
        return f"Job for {self.document.title}"
