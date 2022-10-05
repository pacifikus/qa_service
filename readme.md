## Q&A service

The purpose of the service is to find questions that are as similar as possible to the user's request.

Some requirements and thoughts are placed in [approaches.md]()

### Embedder service

Service to create text embeddings via Tensorflow [Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder/4)

To manual run embedder service:
- Unzip [universal-sentence-encoder_4.tar.gz](https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed) to `models/1` 
- Build docker image with `docker build -t embedder embedder`
- Run docker image with `docker run -t -p 5000:5000 -v "{PROJECT_PWD}/models/1:/models/use" -t embedder`

You can find the Swagger docs on http://localhost:5000/apidocs

To create embedding for the sentence "How many Hindu nations are in the world?" you can run command:

`curl -X POST "http://localhost:5000/v1/embedder/generate" -H "accept: application/json" -H "Content-Type: application/json" -d "{ \"text\": \"How many Hindu nations are in the world?\"}"`

Also, probes are available:
- /readiness - Readiness check endpoint. Make test response to model.
- /liveness - Health check endpoint

