from elasticsearch import Elasticsearch, OrjsonSerializer

client = Elasticsearch(
    hosts=["http://localhost:9200"],
    # basic_auth=(),
    verify_certs=False,
    http_compress=True,
    serializer=OrjsonSerializer(),
    connections_per_node=16,
)

if __name__ == "__main__":
    print(f"{client.info()=}")
    print(f"{client.ping()=}")
