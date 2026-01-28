import json
import time

from ts.context import Context
from ts.torch_handler.base_handler import BaseHandler


class GreeterHandler(BaseHandler):
    def initialize(self, context: Context):
        print(f"greet:initialize:{context}")
        time.sleep(1)
        return "ini"

    def preprocess(self, batch: list[dict]):
        print(f"greet:preprocess:{batch}")
        return [elem["body"] for elem in batch]

    def inference(self, batch: list[bytes], *args, **kwargs):
        print(f"greet:inference:{batch},{args},{kwargs}")
        return [json.loads(x) for x in batch]

    def postprocess(self, batch: list[dict]):
        print(f"greet:postprocess:{batch}")
        time.sleep(0.1)
        return [elem["foo"] for elem in batch]
