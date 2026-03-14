from django.apps import AppConfig
from elasticsearch import Elasticsearch

class PdfReaderConfig(AppConfig):
    name = 'pdf_reader'

    def ready(self):
        es = Elasticsearch(hosts=["http://elastic-search:9200"])

        mapping = {
            "mappings": {
                "properties": {
                    "document_id": {"type": "keyword"},
                    "page_number": {"type": "integer"},
                    "text": {"type": "text"},
                    "embedding": {
                        "type": "dense_vector",
                        "dims": 384,
                        "index": True,
                        "similarity": "cosine"
                    }
                }
            }
        }

        if not es.indices.exists(index="pdf_pages"):
            es.indices.create(index="pdf_pages", body=mapping)