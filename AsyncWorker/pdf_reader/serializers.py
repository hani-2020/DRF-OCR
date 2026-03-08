from rest_framework import serializers
from .models import PDFDocument, ExtractionJob

class UploadPDFSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    def validate(self, attrs):
        file = attrs.get('file')
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return attrs

class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractionJob
        fields = '__all__'