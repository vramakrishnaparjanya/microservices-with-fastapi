# Microservices with FastAPI 🚀

This project demonstrates how to build a **microservices architecture** using **FastAPI** and **Redis Streams**. It showcases a modern approach to developing asynchronous, scalable, and resilient systems using RESTful APIs and event-driven communication.

This repository complements the Medium article:  
[**Microservices using FastAPI and Redis Streams**](https://vramakrishnaparjanya.medium.com/microservices-using-fastapi-and-redis-streams-f15c09206b0e).

---

## Features 🌟
- **FastAPI Framework**: Fast and modern web framework for building APIs with Python.
- **Redis Streams**: Implements event-driven communication between microservices.
- **Asynchronous Programming**: Efficient and high-performance processing using `asyncio`.
- **Scalable Architecture**: Modular design with independent microservices for scalability and maintainability.
- **Swagger UI**: Auto-generated API documentation for seamless testing and development.
- **Dockerized Deployment**: Containerized services for easy setup and deployment.

---

## Prerequisites ⚙️
Before running the application, ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)
- **Docker and Docker Compose** (for containerized setup)
- **Redis** (local or hosted instance)

---

## Getting Started 🚀

### 1. Clone the Repository
```bash
git clone https://github.com/vramakrishnaparjanya/microservices-with-fastapi.git
cd microservices-with-fastapi
```

## Setting Up the Microservices
- Manual Setup
Navigate to Each Service Directory:

```bash
Copy code
cd service_name
```

- Install Dependencies:
```
bash
Copy code
pip install -r requirements.txt
```
- Run the Microservice:

```bash
Copy code
uvicorn main:app --host 0.0.0.0 --port <PORT>
```

Access the API: Visit the Swagger UI at:

```bash
Copy code
http://localhost:<PORT>/docs
```

## Redis Streams Integration
Redis Streams is used for inter-service communication. 
Follow these steps to set up Redis:

- Install Redis:

Install Redis locally or use a cloud-hosted service like Redis Cloud.
Start Redis Server:

```bash
Copy code
redis-server
```

Configure Redis in the Services: Update the Redis connection details in the settings.py or equivalent configuration files.

Run the Event-Driven Microservices: Services will publish and consume events using Redis Streams.


## Related Medium Article 📝
For a detailed walkthrough of this implementation, read the Medium article:
[**Microservices using FastAPI and Redis Streams**](https://vramakrishnaparjanya.medium.com/microservices-using-fastapi-and-redis-streams-f15c09206b0e)

The article covers:
- Setting up FastAPI microservices.
- Integrating Redis Streams for inter-service communication.
