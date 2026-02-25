from fastapi import FastAPI, Query
from app.database import collection
from app.elastic import es, INDEX, create_index
from app.schemas import Product
from app.utils import product_helper

app = FastAPI()


@app.on_event("startup")
def startup():
    create_index()


# ➕ Create Product
@app.post("/products")
def create_product(product: Product):
    mongo_result = collection.insert_one(product.model_dump())

    es.index(
        index=INDEX,
        id=str(mongo_result.inserted_id),
        document=product.model_dump()
    )

    return {"message": "Product created"}


# Search with pagination + fuzzy + filter
@app.get("/search")
def search_products(
    q: str = Query(None),
    category: str = Query(None),
    page: int = 1,
    size: int = 5
):
    must_queries = []

    if q:
        must_queries.append({
            "multi_match": {
                "query": q,
                "fields": ["name"],
                "fuzziness": "AUTO"
            }
        })

    if category:
        must_queries.append({
            "term": {"category": category}
        })

    response = es.search(
        index=INDEX,
        query={"bool": {"must": must_queries}} if must_queries else {"match_all": {}},
        from_=(page - 1) * size,
        size=size
    )

    results = [
        {
            "id": hit["_id"],
            **hit["_source"]
        }
        for hit in response["hits"]["hits"]
    ]

    return results