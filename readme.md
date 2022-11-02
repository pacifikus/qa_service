## Q&A service

The purpose of the service is to find questions that are as similar as possible to the user's request.

### High-level architecture

<p align="center">
  <img src="https://github.com/pacifikus/qa_service/blob/elasticsearch/reference/high-level-diagram.png" width="600" alt="accessibility text">
</p>

Some requirements and thoughts are placed in [approaches.md](https://github.com/pacifikus/qa_service/blob/main/reference/approach.md)

### Clustering

Subproject for data downloading, EDA, embedding clustering, computing clusters centers.

To run data downloading you can follow commands:
```commandline
cd clustering
python src/data/get_data.py --config_path params.yaml
```

To run embeddings computing run:
```commandline
python src/data/create_embeddings.py --config_path params.yaml
```

To create ElasticSearch index with precomputed embeddings run
(you need running ElasticSearch for this step):
```commandline
python src/index/indexer_elastic.py --config_path params.yaml
```


To run embeddings computing run:
```commandline
python src/data/create_embeddings.py --config_path params.yaml
```

To create ElasticSearch index with precomputed embeddings run
(you need running ElasticSearch for this step):
```commandline
python src/index/indexer_elastic.py --config_path params.yaml
```

You can specify configuration in params.yaml if you need

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
Specify user credentials in .env file and create the index with indexer.py script (____coming soon____).

Run streamlit app with `streamlit run search_app/search_companies.py`

You can modify application params in `search_app/params.yaml` if you need
