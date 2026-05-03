# Architecture & Implementation Guide

Tài liệu này hướng dẫn cách tái tạo (replay) toàn bộ hệ thống từ con số 0.

## 1. Core Stack
- **Framework**: FastAPI (HTTP), FastStream (Redis Streams).
- **Vector DB**: LanceDB (File-based).
- **Embedding**: FastEmbed (Model: `BAAI/bge-small-en-v1.5`).
- **Chunking**: LangChain `MarkdownHeaderTextSplitter` & `RecursiveCharacterTextSplitter`.

## 2. LanceDB Schema (MdChunk)
Đây là phần quan trọng nhất để đồng bộ giữa Ingest và Search:

| Field | Type | Role |
| :--- | :--- | :--- |
| `text` | `str` | **SourceField**: Chứa nội dung text và là input cho FTS. |
| `vector` | `Vector(384)` | **VectorField**: Lưu embedding được auto-generate bởi FastEmbed. |
| `filename` | `str` | Tên file để filter và quản lý conflict. |
| `file_hash` | `str` | SHA-256 nội dung file để tránh ingest trùng nội dung. |
| `h1`, `h2`, `h3` | `str` | Lưu cấu trúc header của Markdown để tạo breadcrumb path. |

## 3. Quy trình Ingest (Pipeline)
1. **Validation**: Server nhận file `.md`, kiểm tra trùng tên file trên disk (trả về `409 Conflict`).
2. **Hashing**: Tính SHA-256 nội dung file.
3. **Transfer**: Lưu file vào `./data/uploads/`, gửi message {path, hash, filename} qua Redis.
4. **Worker Processing**:
   - Check duplicate hash trong LanceDB (Skip nếu trùng).
   - **2-Stage Chunking**:
     - B1: Split theo `#`, `##`, `###` (LangChain).
     - B2: Split tiếp các đoạn dài bằng `RecursiveCharacterTextSplitter` (chunk_size=2000 chars, overlap=400 chars).
   - **Indexing**: Sau khi `table.add()`, bắt buộc gọi `table.create_fts_index("text")` để cập nhật Full-Text Search index.

## 4. Quy trình Search (Retrieval)
Hệ thống sử dụng **Hybrid Search (Native LanceDB way)**:
- **Auto-Embedding**: Server không cần tự tính vector, chỉ cần truyền string query vào `table.search(text)`. LanceDB sẽ dùng chính `FastEmbedFunc` đã khai báo trong schema để embed query.
- **RRF (Reciprocal Rank Fusion)**: Kết hợp kết quả từ Vector search và Keyword search.
- **Filtering**: Hỗ trợ filter theo `filename` qua clause `.where()`.
- **Breadcrumb**: UI path được xây dựng bằng cách nối `h1 > h2 > h3`.

## 5. Cấu trúc thư mục dữ liệu
- `./data/uploads/`: Lưu trữ file markdown gốc.
- `./data/lancedb/`: Lưu trữ các file dữ liệu của LanceDB (bao gồm cả các index).

## 6. Lưu ý khi Recreate
- Phải dùng chung một model name (`BAAI/bge-small-en-v1.5`) ở mọi nơi.
- Đảm bảo `tantivy` đã được cài đặt (thường đi kèm `lancedb`) để FTS hoạt động.
- Khi schema thay đổi, nên xóa thư mục `./data/lancedb` để khởi tạo lại từ đầu.
