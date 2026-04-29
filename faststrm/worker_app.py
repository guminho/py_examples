# Import tasks so subscribers get registered on the broker
import worker.tasks  # noqa: F401
from faststream import FastStream
from worker.broker import broker

app = FastStream(broker)
