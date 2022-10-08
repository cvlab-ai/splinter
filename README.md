# Splinter

## Run dockerized environment

```bash
docker-compose up -d
```

To rebuild docker images after updating sources run

```bash
docker-compose up -d --build
```

## Access to web UI

After starting the system, the web application is available under: http://localhost:8000/

test user:
```bash
email: x@x.pl
password: 1
```

## Initialize database

```bash
docker exec -it splinter_db psql -U postgres -d splinter -f db.init
```
