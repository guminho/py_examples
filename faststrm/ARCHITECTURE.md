# Markdown Ingest Pipeline Architecture

Hệ thống xử lý ingest file Markdown tự động, sử dụng kiến trúc Producer-Consumer (FastAPI + FastStream).

## 1. Dòng dữ liệu (Data Flow)

1. **Client**: Upload file `.md` qua `POST /upload`.
2. **FastAPI (Producer)**:
   - Kiểm tra trùng tên file trên disk (`409 Conflict`).
   - Lưu file vào `./data/uploads/`.
   - Tính SHA-256 hash của nội dung file.
   - Gửi message chứa `file_path`, `file_hash`, và `filename` vào Redis Stream `ingest-stream`.
3. **FastStream Worker (Consumer)**:
   - Nhận task từ Redis.
   - Kiểm tra `file_hash` trong LanceDB (Skip nếu đã tồn tại).
   - Đọc file từ shared disk.
   - **Chunking (2 giai đoạn)**:
     - GĐ 1: Tách theo Headers (`#`, `##`, `###`) để giữ ngữ cảnh.
     - GĐ 2: Tách nhỏ các section quá dài (Max 2000 chars ~ 500 tokens).
   - **Embedding**: Sử dụng `FastEmbed` (model `BAAI/bge-small-en-v1.5`) tích hợp trực tiếp vào LanceDB.
   - **Storage**: Lưu vào LanceDB table `md_chunks`.

## 2. Quyết định kỹ thuật (Technical Decisions)

| Thành phần | Lựa chọn | Lý do |
| :--- | :--- | :--- |
| **Giao tiếp** | Redis Streams | Hỗ trợ Consumer Groups, đảm bảo không mất task nếu worker sập. |
| **File Transfer** | Shared Disk | Tiết kiệm băng thông Redis vì worker và server chạy cùng host. |
| **Xử lý trùng** | Filename (Disk) & Hash (DB) | Tránh ghi đè file lung tung và tránh tốn tài nguyên embed lại nội dung cũ. |
| **Embedding** | FastEmbed | Cực nhẹ, không cần PyTorch/Tensorflow, phù hợp cho môi trường serve. |
| **Vector DB** | LanceDB | Dạng file-based (Lance format), tốc độ scan cực nhanh, không cần setup server DB phức tạp. |

## 3. LanceDB Schema (Table: `md_chunks`)

- `text`: Nội dung chunk (Source field).
- `vector`: Vector 384-dim (Auto-generated).
- `filename`: Tên file gốc.
- `file_hash`: SHA-256 để kiểm soát duplicate.
- `h1`, `h2`, `h3`: Metadata header để tái tạo cấu trúc tài liệu khi cần.

## 4. Cấu hình Chunking
- **Chunk Size**: 2000 ký tự (~500 tokens).
- **Chunk Overlap**: 400 ký tự (~100 tokens).
- **Splitter**: `MarkdownHeaderTextSplitter` + `RecursiveCharacterTextSplitter`.
