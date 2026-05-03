from pydantic import BaseModel


class UserRequest(BaseModel):
    user_name: str
    user_id: int


class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    filename: str | None = None


class SearchResult(BaseModel):
    text: str
    score: float
    filename: str
    path: str
