from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")

es = Elasticsearch(ELASTIC_URL)

INDEX_NAME = "products"


def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            mappings={
                "properties": {
                    "name": {"type": "text"},
                    "price": {"type": "float"},
                    "category": {"type": "keyword"},
                }
            },
        )
        print("Index created")