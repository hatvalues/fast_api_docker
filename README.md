# fast_api_docker
A Docker container for FastAPI micro services

## Where are the tests?
Postman collection: My Workspace: FastAPI Docker

## On local with venv

Assume venv is called venv.

`source venv/bin/activate`

`cd app`

`uvicorn app.main:app --host 0.0.0.0 --port 80 --reload`

or

`uvicorn app.main:app --host 0.0.0.0 --port 80`

## On container

launch container:
`docker run -d --name mycontainer -p 80:80 fapi:latest`

## Healthchecks
http://127.0.0.1/
http://127.0.0.1/hello
http://127.0.0.1/items/5?q=somequery
