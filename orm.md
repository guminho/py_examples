# Python ORM Comparison

A detailed comparison of various Python ORM (Object-Relational Mapping) libraries, including their popularity, philosophy, and ideal use cases.

## Main ORMs

| # | Library | Stars (k) | Last CI | Schema | Async | Complexity | Philosophy | Use Case |
|---|---------|-----------|---------|--------|-------|------------|------------|----------|
| 1 | [SQLModel](http://github.com/fastapi/sqlmodel) | 17.5 | 2026-01 | Pydantic + SQLA | Hybrid | Medium | Unified Model | FastAPI (unified models) |
| 2 | [SQLAlchemy](http://github.com/sqlalchemy/sqlalchemy) | 11.4 | 2026-01 | Own | Hybrid | Very High | Power, Flexibility | Complex Enterprise Apps |
| 3 | [Peewee](http://github.com/coleifer/peewee) | 11.9 | 2026-01 | Own | Gevent | Low | Lightweight, Expressive | Small-to-Medium Apps |
| 4 | [Tortoise](http://github.com/tortoise/tortoise-orm) | 5.4 | 2025-12 | Own | ✅ | Medium | Django-inspired | High-perf FastAPI APIs |
| 5 | [Dataset](http://github.com/pudo/dataset) | 4.8 | 2025-02 | Schema-less | ✅ | Minimal | For lazy people | Data-scraping, migration scripts |
| 6 | [PonyORM](http://github.com/ponyorm/pony) | 3.8 | 2025-07 | Own | No | Medium | Pythonic-magic | Rapid Prototyping |
| 7 | [GINO](http://github.com/python-gino/gino) | 2.8 | 2022-02 | Own + SQLA-Core | ✅ | High | Explicitness over magic | Lightweight async logic |
| 8 | [Piccolo](http://github.com/piccolo-orm/piccolo) | 1.9 | 2026-01 | Own + Pydantic | ✅ | Medium | Batteries-included | Full-stack with Admin UI |
| 9 | [Ormar](http://github.com/collerek/ormar) | 1.8 | 2026-01 | Pydantic + SQLA-Core | ✅ | Medium | Pydantic pioneer | Pydantic-first async apps |

## Others & Archived

| # | Library | Stars (k) | Last CI | Status |
|---|---------|-----------|---------|--------|
| 1 | [pyDAL](http://github.com/web2py/pydal) | 0.5 | 2025-12 | Active |
| 2 | [Edgy](https://github.com/dymmond/edgy) | 0.4 | 2025-11 | Active |
| 3 | [Saffier](https://github.com/tarsil/saffier) | 0.15 | 2025-04 | Active |
| 4 | [Prisma](http://github.com/RobertCraigie/prisma-client-py) | 2.1 | 2025-03 | ARCHIVED |
| 5 | [Databases](http://github.com/encode/databases) | 4 | 2024-03 | ARCHIVED |
| 6 | [ORM](http://github.com/encode/orm) | 1.9 | 2022-08 | ARCHIVED |
| 7 | [Orator](https://github.com/sdispater/orator) | 1.4 | 2022-03 | ARCHIVED |

---
*Extracted from the main README.*
