import rich
from cli import client

INDEX = "book_index"

# Match query
# match. The standard query for performing full text queries, including fuzzy matching and phrase or proximity queries.
# multi-match. The multi-field version of the match query.

resp = client.search(
    index=INDEX,
    query={"match": {"summary": {"query": "guide"}}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


resp = client.search(
    index=INDEX,
    query={"multi_match": {"query": "javascript", "fields": ["summary", "title^3"]}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Term search
# Returns document that contain exactly the search term.

resp = client.search(
    index=INDEX,
    query={"term": {"publisher.keyword": "addison-wesley"}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Range search
# Returns documents that contain terms within a provided range.

resp = client.search(
    index=INDEX,
    query={"range": {"num_reviews": {"gte": 45}}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Prefix search
# Returns documents that contain a specific prefix in a provided field

resp = client.search(
    index=INDEX,
    query={"prefix": {"title": {"value": "java"}}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Fuzzy search
# Returns documents that contain terms similar to the search term,
# as measured by a Levenshtein edit distance.

resp = client.search(
    index=INDEX,
    query={"fuzzy": {"title": {"value": "pyvascript"}}},
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# bool.must (AND)
resp = client.search(
    index=INDEX,
    query={
        "bool": {
            "must": [
                {"term": {"publisher.keyword": "addison-wesley"}},
                {"term": {"authors.keyword": "richard helm"}},
            ]
        }
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# bool.should (OR)
resp = client.search(
    index=INDEX,
    query={
        "bool": {
            "should": [
                {"term": {"publisher.keyword": "addison-wesley"}},
                {"term": {"authors.keyword": "douglas crockford"}},
            ]
        }
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# bool.filter
resp = client.search(
    index=INDEX,
    query={
        "bool": {
            "filter": [
                {"term": {"publisher.keyword": "prentice hall"}},
            ],
        }
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# bool.must_not
resp = client.search(
    index=INDEX,
    query={
        "bool": {
            "must_not": [
                {"range": {"num_reviews": {"lte": 45}}},
            ]
        }
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])


# Using Filters with Queries
resp = client.search(
    index=INDEX,
    query={
        "bool": {
            "must": [{"match": {"title": {"query": "javascript"}}}],
            "must_not": [{"range": {"num_reviews": {"lte": 45}}}],
        }
    },
    source_excludes=["title_vector"],
)
rich.print(resp["hits"])
