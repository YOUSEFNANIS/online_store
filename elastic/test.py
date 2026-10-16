"""
Load NASA APOD (Astronomy Picture of the Day) JSON data into Elasticsearch.

Requires:
    pip install elasticsearch

Assumes:
    - An Elasticsearch instance running and reachable (default: http://localhost:9200)
    - Input file: apod.json -> a JSON array of objects with fields:
        date, title, explanation, image_url, authors
"""

import json
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

# ---------------------------------------------------------------------------
# STEP 1: Connect to Elasticsearch
# ---------------------------------------------------------------------------
# Change the host/port/credentials to match your cluster.
# For a local Elastic Cloud / Docker instance without auth, this is enough.
# For Elastic Cloud, you'd typically use `cloud_id` + `api_key` instead.
es = Elasticsearch(
    "http://127.0.0.1:9200"
)

# Sanity check the connection early, so we fail fast with a clear message
if not es.ping():
    raise ConnectionError(
        "Could not connect to Elasticsearch. "
        "Check that it's running and the host/credentials are correct."
    )

INDEX_NAME = "apod"

mapping = {
    "mappings": {
    }
}

# Drop the index if it already exists, so re-running this script is idempotent
if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)

es.indices.create(index=INDEX_NAME, body=mapping)


# ---------------------------------------------------------------------------
# STEP 3: Load the JSON file from disk
# ---------------------------------------------------------------------------
with open("clothes.json", "r", encoding="utf-8") as f:
    records = json.load(f)


# ---------------------------------------------------------------------------
# STEP 5: Bulk index the documents
# ---------------------------------------------------------------------------
# Using the `date` field as the document _id keeps loading idempotent:
# re-running the script updates existing docs instead of creating duplicates
# (though we already delete+recreate the index above, this is good practice
# in general, e.g. for incremental loads).
def generate_actions(docs):
    for i, doc in enumerate(docs):
        print(i)
        yield {
            "_index": INDEX_NAME,
            "_id": i,
            "_source": doc,
        }


success, errors = helpers.bulk(
    es,
    generate_actions(records),
    raise_on_error=False,
)


# ---------------------------------------------------------------------------
# STEP 6: Refresh the index and verify
# ---------------------------------------------------------------------------
# Elasticsearch refreshes automatically every ~1s, but calling refresh()
# explicitly makes newly indexed docs immediately searchable/countable.
es.indices.refresh(index=INDEX_NAME)

count = es.count(index=INDEX_NAME)["count"]
print(f"Total documents in '{INDEX_NAME}' index: {count}")

# Quick sanity-check search
sample = es.search(
    index=INDEX_NAME,
    query={"match": {"explanation": "galaxy"}},
    size=3,
)
response = es.search(
    index='apod',
    query={
        'bool': {
            'filter':
                [{
                    'match':{'model': 'model_1'}
                }]
            
        }
    }
)

print(response.keys())