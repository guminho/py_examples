from contextlib import asynccontextmanager
from enum import StrEnum
from typing import Optional

from beanie import Document, PydanticObjectId, init_beanie
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import AsyncMongoClient


class TagColors(StrEnum):
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"


class Tag(BaseModel):
    name: str
    color: TagColors = TagColors.BLUE


class Note(Document):
    title: str
    text: Optional[str]
    tag_list: list[Tag] = []

    class Settings:
        name = "notes"


class AggregationResponseItem(BaseModel):
    id: str = Field(None, alias="_id")
    total: int


router = APIRouter()

# CRUD


async def get_note(note_id: PydanticObjectId) -> Note:
    if note := await Note.get(note_id):
        return note
    raise HTTPException(status_code=404, detail="Note not found")


@router.post("/notes/")
async def create_note(note: Note) -> Note:
    await note.insert()
    return note


@router.get("/notes/{note_id}")
async def get_note_by_id(note: Note = Depends(get_note)) -> Note:
    return note


@router.put("/notes/{note_id}/add_tag")
async def add_tag(tag: Tag, note: Note = Depends(get_note)) -> Note:
    print(f"tag:{[tag]}")
    await note.update({"$push": {"tag_list": tag.model_dump()}})
    return note


class Statuses(StrEnum):
    DELETED = "DELETED"


@router.delete("/notes/{note_id}")
async def delete_note(note: Note = Depends(get_note)):
    await note.delete()
    return dict(status=Statuses.DELETED)


# LIST


@router.get("/notes/")
async def list_notes_all() -> list[Note]:
    return await Note.find_all().to_list()


@router.get("/notes/by_tag/{tag_name}")
async def filter_notes_by_tag(tag_name: str) -> list[Note]:
    return await Note.find_many({"tag_list.name": tag_name}).to_list()


# AGGREGATIONS


@router.get("/notes/aggregate/by_tag_name")
async def filter_notes_by_tag_name() -> list[AggregationResponseItem]:
    return await Note.aggregate(
        aggregation_pipeline=[
            {"$unwind": "$tag_list"},
            {"$group": {"_id": "$tag_list.name", "total": {"$sum": 1}}},
        ],
        projection_model=AggregationResponseItem,
    ).to_list()


@router.get("/notes/aggregate/by_tag_color")
async def filter_notes_by_tag_color() -> list[AggregationResponseItem]:
    return await Note.aggregate(
        aggregation_pipeline=[
            {"$unwind": "$tag_list"},
            {"$group": {"_id": "$tag_list.color", "total": {"$sum": 1}}},
        ],
        projection_model=AggregationResponseItem,
    ).to_list()


MONGO_DSN = "mongodb://demo:changeme@localhost"


@asynccontextmanager
async def lifespan(app):
    # INIT MONGO
    cli = AsyncMongoClient(MONGO_DSN)
    await init_beanie(cli["beanie_db"], document_models=[Note])

    try:
        yield
    finally:
        await cli.close()


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/v1", tags=["notes"])
