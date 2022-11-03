# Q&A service

The purpose of the service is to find questions that are as similar as possible to the user's request.

## High-level architecture

<p align="center">
  <img src="https://github.com/pacifikus/qa_service/blob/elasticsearch/reference/high-level-diagram.png" width="600" alt="accessibility text">
</p>

Some requirements and thoughts are placed in [approaches.md](https://github.com/pacifikus/qa_service/blob/main/reference/approach.md)

## Key parts description

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

You can specify configuration in params.yaml if you need

### Embedder service

Service to create text embeddings via Tensorflow [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4)

Consume messages from [RabbitMQ](https://www.rabbitmq.com/) queue, and publish reply to the queue via [RPC mode](https://www.rabbitmq.com/tutorials/tutorial-six-python.html).

### Search streamlit app

[Streamlit](https://streamlit.io/) application to find nearest StackOverflow question.

The application needs [ElasticSearch](https://www.elastic.co/) index to search by.

You can modify application params in `search_app/params.yaml` if you need

## How to run

You can run any services in the single mode, see [reference](/reference/single_mode_run.md)

To run all with docker-compose run

- Specify ElasticSearch user credentials in `clustering/.env` and `/es.env` files
- Run all containers with `docker-compose up`
- Create ElasticSearch index with command `python src/index/indexer_elastic.py --config_path params.yaml`

Finally, your search_app service will be deployed on localhost:8501
