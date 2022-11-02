## Few requirements:
- The most similar questions should be given to the user's request
- The service stores all question-answer pairs by default
- The service has fast response time
- Knowledge base grows over time (and duplicates accumulate)
- New topics are added to the database, and some are deleted
- Some parts of computation are moved to offline

## Offline part

- Computing of embeddings for all documents
- Clustering all documents embeddings and computing clusters centers
- Creation of embeddings indexes
- Computing question-answer mapping


## Online part

- When a request comes from a user, we get its embedding via `Embedder` service and look for the nearest cluster of questions and answers.
- When the cluster is found, we take k nearest neighbors inside it.
- After that we rank the found neighbors and return result.
