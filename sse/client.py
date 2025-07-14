from httpx import Client
from httpx_sse import connect_sse

cli = Client()


def main():
    url = "http://localhost:8000/chat"
    params = {"name": "world"}
    with connect_sse(cli, "POST", url, params=params) as event_source:
        for sse in event_source.iter_sse():
            print(sse.json())


main()
