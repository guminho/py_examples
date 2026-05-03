import hashlib
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, UploadFile
from worker.constants import INGEST_STREAM

UPLOAD_DIR = Path("./data/uploads")

router = APIRouter()


@router.post("/upload")
async def upload_markdown(file: UploadFile, request: Request):
    # Validate file extension
    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are accepted")

    # Check duplicate filename on disk
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    dest = UPLOAD_DIR / file.filename
    if dest.exists():
        raise HTTPException(
            status_code=409, detail=f"File '{file.filename}' already exists"
        )

    # Read content and compute hash
    content = await file.read()
    file_hash = hashlib.sha256(content).hexdigest()

    # Save to disk
    dest.write_bytes(content)

    # Publish ingest task to Redis stream
    broker = request.app.state.broker
    await broker.publish(
        {
            "file_path": str(dest.resolve()),
            "file_hash": file_hash,
            "filename": file.filename,
        },
        stream=INGEST_STREAM,
    )

    return {"status": "queued", "filename": file.filename, "file_hash": file_hash}
