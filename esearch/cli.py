from elasticsearch import Elasticsearch, OrjsonSerializer

PWD = "CHANGE_ME"
client = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", PWD),
    verify_certs=False,
    http_compress=True,
    serializer=OrjsonSerializer(),
    connections_per_node=16,
)
