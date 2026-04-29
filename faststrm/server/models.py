from pydantic import BaseModel


class UserRequest(BaseModel):
    user_name: str
    user_id: int
