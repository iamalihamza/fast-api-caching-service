# fast-api-caching-service

A simple caching microservice built with FastAPI and SQLModel that transforms and interleaves two lists of strings. The service caches transformed results in a SQLite database. This project is containerized using Docker.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- (Optional) Python 3.10+ and pip (if you want to run the service/tests outside Docker)

## Project Structure

- **app/** – Contains the FastAPI application code
  - `main.py` – API endpoints and application startup logic
  - `crud.py` – Business logic for caching and payload management
  - `database.py` – Database configuration and session management
  - `models.py` – SQLModel models for the database tables
  - `schemas.py` – Pydantic models for request and response validation
- **tests/** – Contains pytest tests for the API endpoints
- **Dockerfile** – Docker configuration to build and run the container
- **requirements.txt** – Python dependencies

## Building the Docker Image

From the project root directory, run:

```bash
docker build --no-cache -t caching_service .
```

## Running the Docker Image
From the project root directory, run:
```bash
docker run --name <container_name> -d caching_service
```

## Testing Inside Docker Container
From the project root directory, run:
```bash
docker exec -it <container_name> bash
```
Once inside the Docker container, run:
```bash
pytest tests/
```