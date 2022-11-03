### Embedder service

Service to create text embeddings via Tensorflow [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4)

To manual run embedder service:
- Unzip [universal-sentence-encoder_4.tar.gz](https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed) to `models/1`
- Build docker image with `docker build -t embedder embedder`
- Run docker image with `docker run -t -p 5000:5000 -v "{PROJECT_PWD}/models/1:/models/use" -t embedder`

You can find the Swagger docs on http://localhost:5000/apidocs

To create embedding for the sentence "How many Hindu nations are in the world?" you can run command:

```
curl -X POST "http://localhost:5000/v1/embedder/generate" -H "accept: application/json"\
-H "Content-Type: application/json" -d "{ \"text\": \"How many Hindu nations are in the world?\"}"
```

Also, probes are available:
- /readiness - Readiness check endpoint. Make test response to model.
- /liveness - Health check endpoint


### Search streamlit app

[Streamlit](https://streamlit.io/) application to find nearest StackOverflow question.

The application needs [ElasticSearch](https://www.elastic.co/) index to search by.

#### ElasticSearch installation

To install ElasticSearch locally in single node mode use:
```commandline
docker run --name es01 -p 9200:9200 -p 9300:9300  -e "discovery.type=single-node" -t elasticsearch:8.4.3
```

Specify user credentials in .env file and create the index from pre-computed embeddings with the command:
```commandline
python src/index/indexer_elastic.py --config_path params.yaml
```

Run streamlit app with `streamlit run search_app/search_companies.py`

You can modify application params in `search_app/params.yaml` if you need
