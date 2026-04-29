from fastapi import APIRouter, Request
from worker.constants import GOODBYE_STREAM, GREETING_STREAM

from server.models import UserRequest

router = APIRouter()


@router.post("/send")
async def send_messages(user: UserRequest, request: Request):
    broker = request.app.state.broker
    payload = user.model_dump()

    # Publish 2 greetings + 1 goodbye
    await broker.publish(payload, stream=GREETING_STREAM)
    await broker.publish(payload, stream=GREETING_STREAM)
    await broker.publish(payload, stream=GOODBYE_STREAM)

    return {"status": "ok", "published": 3}
