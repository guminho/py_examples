from pydantic import BaseModel


class GreetingMessage(BaseModel):
    user_name: str
    user_id: int


class GoodbyeMessage(BaseModel):
    user_name: str
    user_id: int


class IngestMessage(BaseModel):
    file_path: str
    file_hash: str
    filename: str
