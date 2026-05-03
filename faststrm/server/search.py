import lancedb
from fastapi import APIRouter, Request
from lancedb.rerankers import RRFReranker
from worker.embeddings import FastEmbedFunc

from server.models import SearchRequest, SearchResult

router = APIRouter()
func = FastEmbedFunc.create()
reranker = RRFReranker()


@router.post("/search", response_model=list[SearchResult])
async def search_markdown(query: SearchRequest, request: Request):
    # 1. Get LanceDB table from app state
    table: lancedb.table.Table = request.app.state.md_chunks_table

    # 2. Build the query using native auto-embedding
    # Since we registered FastEmbedFunc in the schema, LanceDB will auto-embed the query string
    search_query = table.search(
        query.query,
        query_type="hybrid",
        vector_column_name="vector",
        fts_columns="text",
    ).rerank(reranker)

    # 4. Apply optional filename filter
    if query.filename:
        # Note: LanceDB uses SQL-like syntax for where clause
        search_query = search_query.where(f"filename = '{query.filename}'")

    # 5. Execute search with limit
    results = search_query.limit(query.limit).to_list()

    # 6. Format results with breadcrumb path
    formatted_results = []
    for row in results:
        # Build path: H1 > H2 > H3
        headers = [row.get("h1"), row.get("h2"), row.get("h3")]
        path_segments = [h for h in headers if h]
        breadcrumb = (
            " > ".join(path_segments) if path_segments else row.get("filename", "")
        )

        formatted_results.append(
            SearchResult(
                text=row["text"],
                score=row.get("_distance", 0.0),  # LanceDB returns score in _distance
                filename=row["filename"],
                path=breadcrumb,
            )
        )

    return formatted_results
