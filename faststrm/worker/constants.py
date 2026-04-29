import os
from uuid import uuid4

GREETING_STREAM = "greeting-stream"
GOODBYE_STREAM = "goodbye-stream"

GREETING_GROUP = "greeting-group"
GOODBYE_GROUP = "goodbye-group"
CONSUMER_NAME = os.environ.get("CONSUMER_NAME", f"consumer-{uuid4().hex[:8]}")
