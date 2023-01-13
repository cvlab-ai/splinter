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

## Testing

Run integration tests by:

```bash
pytest -v -s tests/
```

## Deploy

To prepare the project for deploying run the `deploy_setup.sh` script:

```bash
./deploy_setup.sh
```

The script will:

* generate random passwords for docker services & replace them in `.env` file
* generate docker-compose file compatible with docker swarm e.g include the
  content of .env file to each service depending on it.

**NOTE: Remember to save generated passwords!**
