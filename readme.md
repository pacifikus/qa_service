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

You can find the Swagger docs on http://localhost:5000/apidocs

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

## Testing

### Load tests

There is load test written with [Locust](https://locust.io/) in the `tests/locustfile.py`.
To run test follow these steps:
- install locust with `pip install locust`
- go to `tests` folder
- run locust web UI with command `locust`
- open `http://localhost:8089/` and specify test params (Number of users, Spawn rate, Host with running search server)
- start swarming

Also, you can run load tests without web UI, see [Locust docs](https://docs.locust.io/en/stable/running-without-web-ui.html#running-without-web-ui)


[Here](reference/load_testing_report.html) you can see current load testing result with such hardware configuration:

- CPU: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz   2.59 GHz
- RAM: 16 GB
- System disk space: 20 GB
