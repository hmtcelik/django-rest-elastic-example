# Django REST and Elasticsearch example

This is a simple example of how to use Django REST and Elasticsearch to search for with a keyword.

## USAGE:

### Prerequisites:

Don't forget to create a `.env` file with the following variables:

```bash
# .env
SECRET_KEY=your_secret_key
```

### 1. Get ready the containers:

```bash
docker-compose up --build
```
before continue, wait for everything ready (the elasticsearch wake up may tooks a few seconds)

### 2. Create the indexes:

(Not required for tests)

```bash
docker-compose exec api python manage.py create_indexes
```

### 3. Search in Elasticsearch via "management command" or endpoint:

```bash
docker-compose exec api python manage.py search_hostname <username> <password> <hostname>
```

### or you can just use the endpoint:

```bash
curl --request POST \
  --url http://localhost:8000/api/search/ \
  --header 'Authorization: Octoxlabs <base64_token>' \
  --header 'Content-Type: application/json' \
  --data '{
        "query": "Hostname = octoxlabs*"
}'
```

### 4. (OPTIONAL) Run the tests:

```bash
docker-compose exec api python manage.py test
```
