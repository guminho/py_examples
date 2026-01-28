from random import randrange

import rich
from cli import client
from elasticsearch import helpers
from elasticsearch.esql import ESQL

IDX = "employees"
FIRST_NAMES = ["Alyssa", "Jessica", "Katrina", "Mariah", "Zachary"]
LAST_NAMES = ["Brown", "Hinton", "Lopez", "Patel", "Wallace"]


def ini():
    o = client.indices.create(index=IDX)
    print(o)


def add_many():
    def gen():
        for last_name in LAST_NAMES:
            for first_name in FIRST_NAMES:
                yield {
                    "_index": IDX,
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": randrange(14, 30),
                    "height": round(randrange(160, 190, 2) / 100, 2),
                }

    o = helpers.bulk(client, gen())
    print(o)


def search():
    query = (
        ESQL.from_(IDX)
        .where("age >= 26")
        .sort("age")
        .eval(height_cm="height * 100")
        .limit(3)
        .keep("first_name", "last_name", "height_cm")
    )
    rich.print(query)
    o = client.esql.query(query=query)
    rich.print(o)


if __name__ == "__main__":
    # ini()
    # add_many()
    search()
