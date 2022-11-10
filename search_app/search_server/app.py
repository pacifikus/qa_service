import json

import requests
import yaml
from elastic_client import ElasticClient
from flask import Flask, jsonify, request

app = Flask(__name__)
config_path = "params.yaml"

with open(config_path) as conf_file:
    config = yaml.safe_load(conf_file)

elastic_client = ElasticClient(
    host=config["indexing"]["elastic"]["host"],
    https=config["indexing"]["elastic"]["https"],
    config_path=config["indexing"]["vector_config_path"],
)


def get_query_config(query_vector, docs_count, distance_metric):
    if distance_metric == "Cosine similarity":
        distance_metric = "1.0 + cosineSimilarity(params['query_vector'], 'vector')"
    elif distance_metric == "l1norm":
        distance_metric = "1 / (1 + l1norm(params.query_vector, 'vector'))"
    elif distance_metric == "l2norm":
        distance_metric = "1 / (1 + l2norm(params.query_vector, 'vector'))"
    else:
        distance_metric = (
            "double value = dotProduct(params.query_vector, 'vector');"
            " return sigmoid(1, Math.E, -value);"
        )
    es_query = {
        "size": docs_count,
        "_source": ["post_id", "text", "vector"],
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": distance_metric,
                    "params": {"query_vector": query_vector},
                },
            }
        },
    }

    return es_query


def get_query_embedding(input_query):
    input_query = input_query.lower()
    data = {"text": input_query}
    headers = {"Accept": "application/json"}
    response = json.loads(
        requests.post(
            url=config["embedder"]["url"],
            json=data,
            headers=headers,
        ).text
    )
    query_vector = response["outputs"][0][0]
    return query_vector


@app.route("/find", methods=["POST"])
def start_search():
    data = request.get_json(force=True)

    fields = ["query", "n_docs", "distance", "index"]

    for field in fields:
        if field not in data or data[field] == "":
            return jsonify(error=f"Field {field} is required!"), 400

    query_embedding = get_query_embedding(data["query"])
    query = get_query_config(
        query_embedding, docs_count=data["n_docs"], distance_metric=data["distance"]
    )
    docs, query_time, num_found = elastic_client.query(data["index"], query)
    return jsonify(
        docs=docs,
        query_time=query_time,
        num_found=num_found,
        query_embedding=query_embedding,
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
