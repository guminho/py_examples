import rich
from cli import client
from elasticsearch import helpers

IDX = "my-idx-abc"
print(client.info())


def ini():
    o = client.indices.create(index=IDX)
    print(o)


def add_one():
    o = client.index(
        index=IDX,
        id="my_document_id",
        document={"foo": "foo", "bar": "bar"},
    )
    print(o)


def add_many():
    def gen():
        for i in range(10):
            yield {"_index": IDX, "foo": f"foo {i}", "bar": "bar"}

    o = helpers.bulk(client, gen())
    print(o)


def get_one():
    o = client.get(index=IDX, id="my_document_id")
    rich.print(o)


def update_one():
    o = client.update(
        index=IDX,
        id="my_document_id",
        doc={
            "foo": "bar",
            "new_field": "new value",
        },
    )
    print(o)


def del_one():
    o = client.delete(index=IDX, id="my_document_id")
    print(o)


def search():
    o = client.search(
        index=IDX,
        from_=2,
        size=5,
        query={"match": {"foo": "foo"}},
    )
    rich.print(o["hits"]["hits"])


if __name__ == "__main__":
    # ini()
    # add_one()
    # add_many()
    # update_one()
    # del_one()

    get_one()
    search()
