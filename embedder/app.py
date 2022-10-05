import tensorflow_hub as hub
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from exceptions import HealthError


MODEL_PATH = "models/use"
embedder = hub.load(MODEL_PATH)

app = Flask(__name__)
app.config["SWAGGER"] = {
    "title": "use-embedder",
}
swag = Swagger(app)


def generate_embedding(text):
    return embedder([text]).numpy().tolist()


@app.route("/liveness", methods=["GET"])
@swag_from("docs/liveness.yml")
def health_check():
    return "Ok", 200


@app.route("/readiness", methods=["GET"])
@swag_from("docs/readiness.yml")
def readiness_check():
    text = "How many Hindu nations are in the world?"
    try:
        generate_embedding(text)
    except HealthError as exception:
        return str(exception), 503
    else:
        return "Ready", 200


@app.route('/v1/embedder/generate', methods=['POST'])
@swag_from("docs/generate.yml")
def generate():
    data = request.get_json(force=True)
    embedding = generate_embedding(data['text'])
    return jsonify(outputs=[embedding])


if __name__ == "__main__":
    app.run()
