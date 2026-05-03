# FastStream + LanceDB Markdown RAG

A lightweight RAG (Retrieval-Augmented Generation) pipeline for Markdown files using FastAPI, FastStream (Redis), and LanceDB.

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Start the Worker** (Processes uploads, chunks markdown, and indexes vectors):
   ```bash
   cd faststrm
   faststream run worker_app:app
   ```

3. **Start the Server** (FastAPI publisher and search API):
   ```bash
   cd faststrm
   uvicorn server_app:app
   ```

## 🛠 API Usage Examples

### 1. Upload a Markdown File
Uploads a file, saves it to disk, and triggers the ingest background task.
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@path/to/your-file.md"
```

### 2. Hybrid Search
Performs a hybrid search (Vector + Full-Text Search) with optional filename filtering.
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "what is a subagent",
    "limit": 3
  }'
```

### 3. Search with Filename Filter
Limit the search results to a specific document.
```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "context engineering",
    "filename": "deepa-context-engineering.md",
    "limit": 2
  }'
```

## 📖 Documentation
For a deep dive into the system design and how to recreate this project from scratch, see [ARCHITECTURE.md](./ARCHITECTURE.md).
