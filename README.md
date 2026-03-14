# Async PDF OCR & Semantic Search Engine 📄🔍

A powerful, asynchronous PDF processing system built with Django, Celery, and Elasticsearch. This project allows users to upload PDF documents, automatically extract text using Tesseract OCR with OpenCV preprocessing, generate vector embeddings for semantic search, and index the content for high-performance hybrid (full-text + vector) search.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?style=for-the-badge&logo=django)
![Celery](https://img.shields.io/badge/Celery-Asynchronous-green?style=for-the-badge&logo=celery)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-Search_Engine-005571?style=for-the-badge&logo=elasticsearch)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue?style=for-the-badge&logo=docker)

---

## ✨ Features

- **🚀 Asynchronous Processing**: Large PDFs are handled in the background using Celery workers, ensuring the API remains responsive.
- **👁️ Advanced OCR**: Utilizes Tesseract OCR for text extraction.
- **🖼️ Image Preprocessing**: Uses OpenCV (adaptive thresholding) to improve OCR accuracy by cleaning up page images.
- **📊 Real-time Progress**: Stream extraction progress in real-time via Server-Sent Events (SSE).
- **🔎 Hybrid Search**: Combines traditional BM25 full-text search with AI-powered KNN vector search for more accurate and context-aware results.
- **🧠 Vector Embeddings**: Automatically generates semantic embeddings for every page using the `all-MiniLM-L6-v2` model.
- **🛠️ Scalable Architecture**: Containerized setup with RabbitMQ as a message broker and dedicated worker services.

---

## 🛠️ Tech Stack

- **Backend**: Django & Django REST Framework (DRF)
- **Task Queue**: Celery
- **Message Broker**: RabbitMQ
- **Search Engine**: Elasticsearch with KNN support
- **AI/ML**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **OCR Engine**: Tesseract OCR
- **Image Processing**: OpenCV, Pillow, pdf2image
- **DevOps**: Docker & Docker Compose

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd DRFPractice
   ```

2. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```

3. **Access the services**:
   - **Django API**: `http://localhost:8000`
   - **RabbitMQ Management**: `http://localhost:15672` (User: `user`, Pass: `password`)
   - **Elasticsearch**: `http://localhost:9200`

---

## 📡 API Documentation

### 1. Upload PDF
- **Endpoint**: `POST /api/upload/`
- **Body**: `file` (Multipart/form-data)
- **Response**: Returns a `job_id` to track progress.

### 2. Track Extraction Progress (SSE)
- **Endpoint**: `GET /api/job/<job_id>/`
- **Description**: Streams real-time updates of the extraction status and progress percentage.

### 3. Search Extracted Text
- **Endpoint**: `GET /api/search/?q=<query>`
- **Description**: Performs a **hybrid search** across all processed documents. It combines:
    - **Keyword Matching**: Phrase prefix and full-text matches.
    - **Semantic Search**: KNN vector comparison using 384-dimensional embeddings to find contextually relevant content even if exact keywords don't match.

### 4. List Documents
- **Endpoint**: `GET /api/files/`
- **Description**: Returns a list of all uploaded and processed PDF documents.

---

## 🏗️ Project Structure

```text
.
├── AsyncWorker/
│   ├── pdf_reader/          # Main application logic (models, tasks, views)
│   ├── AsyncWorkerProject/  # Project settings
│   ├── Dockerfile           # Python/Django container config
│   └── requirements.txt     # Python dependencies
├── docker-compose.yml       # Orchestration for Django, Celery, RabbitMQ, ES
└── README.md                # You are here!
```

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
