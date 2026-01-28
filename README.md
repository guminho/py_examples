# PYTHON EXAMPLES

## 1. Catalog

|  |  |  |  |
|--|--|--|--|
|audio|scheduler|mongodb|[orm](#4-orm)
|jwt|http2|server-sent-events|[requestx](requestx/README.md)
|[prometheus](prom/readme.md)|[torch-serve](torchsrv/README.md)|[triton-serve](tritonsrv/README.md)|


## 2. Setup

```bash
python3 -m venv venv
. venv/bin/activate

# or
uv sync
```


## 3. Usage

### JWT

```bash
cd jwt2
bash genkey.sh
python main.py
```

### HTTP/2

```bash
cd h2
bash gencert.sh
hypercorn server:app -c hyper.toml

# client
curl https://localhost:8000/ -i -k
```

### Server-Sent-Event

```bash
cd sse
uvicorn server:app --log-config=log-config.yml

# client
curl localhost:8000?name=world -i -X POST
python client.py
```

### Scheduler

```bash
cd sched
python blocking.py
python thread.py
```


## 4. ORM

@ |lib                                                  |kstars|last-ci|schema              |async |complexity|philosophy             |use-case
--|--                                                   |--    |--     |--                  |--    |--        |--                     |--
1 |[sqlmodel](http://github.com/fastapi/sqlmodel)       |17.5  |2026-01|pydantic + sqla     |hybrid|medium    |unified-model          |fastapi (unified models)
2 |[sqlalchemy](http://github.com/sqlalchemy/sqlalchemy)|11.4  |2026-01|own                 |hybrid|very high |power, flexibility     |complex enterprise apps
3 |[peewee](http://github.com/coleifer/peewee)          |11.9  |2026-01|own                 |gevent|low       |lightweight, expressive|small-to-medium apps
4 |[tortoise](http://github.com/tortoise/tortoise-orm)  |5.4   |2025-12|own                 |✅    |medium    |django-inspired        |high-perf fastapi apis
5 |[dataset](http://github.com/pudo/dataset)            |4.8   |2025-02|schema-less         |✅    |minimal   |for lazy people        |data-scraping, migration scripts
6 |[ponyorm](http://github.com/ponyorm/pony)            |3.8   |2025-07|own                 |no    |medium    |pythonic-magic         |rapid prototyping
7 |[gino](http://github.com/python-gino/gino)           |2.8   |2022-02|own + sqla-core     |✅    |high      |explicitness over magic|lightweight async logic
8 |[piccolo](http://github.com/piccolo-orm/piccolo)     |1.9   |2026-01|own + pydantic      |✅    |medium    |batteries-included     |full-stack with admin ui
9 |[ormar](http://github.com/collerek/ormar)            |1.8   |2026-01|pydantic + sqla-core|✅    |medium    |pydantic pioneer       |pydantic-first async apps

### others

@ |lib                                                                 |kstars|last-ci
--|--                                                                  |--    |--
1 |[pydal](http://github.com/web2py/pydal)                             |0.5   |2025-12
2 |[edgy](https://github.com/dymmond/edgy)                             |0.4   |2025-11
3 |[saffier](https://github.com/tarsil/saffier)                        |0.15  |2025-04
4 |[prisma](http://github.com/RobertCraigie/prisma-client-py)-ARCHIVED |2.1   |2025-03
5 |[databases](http://github.com/encode/databases)-ARCHIVED            |4     |2024-03
6 |[orm](http://github.com/encode/orm)-ARCHIVED                        |1.9   |2022-08
7 |[orator](https://github.com/sdispater/orator)-ARCHIVED              |1.4   |2022-03
