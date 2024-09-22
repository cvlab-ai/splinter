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

After starting the system, the web application is available under: http://localhost:8888/splinter

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

## Training
MobileNetV3Small under research/mark_generator/00_training.ipynb

## Known Issues

- **Issue: `exec /docker-entrypoint.sh: no such file or directory` after running the Docker containers**

    For detailed troubleshooting steps and solution, refer to this [Stack Overflow post](https://stackoverflow.com/questions/38905135/why-wont-my-docker-entrypoint-sh-execute).

- **Unresolved References in IDE:**
    
    If you encounter unresolved references in your IDE (like PyCharm), follow these steps to resolve the issue:
    1. Open PyCharm and navigate to `File -> Settings -> Project:Splinter -> Project Structure`.
    2. Locate the `inference_engine` module within your project structure.
    3. Mark `inference_engine` as `Sources root`
    
    This action informs PyCharm that the `inference_engine` module should be recognized as a source directory, resolving unresolved references and enabling proper module imports within your project.

