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

## Development

### Changing the Model

The models used by the inference engine are located in the `inference_engine/data/model` directory, for example, `inference_engine/data/model/answer-checking-model.pt`.

To change the model, follow these steps:

1. **Replace the Model File**

    Replace the existing model file with the new model file in the `inference_engine/data/model` directory.

2. **Update the Configuration File**

    Update the path to the new model file in the `config.yaml` file under the paths section. For example, to change the box_model_path, modify it as follows:
    ```yaml
   paths:
     box_model_path: inference_engine/data/model/your-new-model-file.pt
   ```

### Deploying Docker Images to Docker Hub

To deploy the Docker images to Docker Hub, follow these steps:

1. **Log in to Docker Hub**

   First, log in to your Docker Hub account:
   ```sh
   docker login
   ```
    Enter your username and password/token.  If you have 2FA enabled, generate a Personal Access Token in Docker 
2. **Build the Docker Images**

    Build the images with appropriate tags pointing to your repository. Navigate to the folder containing your `docker-compose-prod.yml` and run:
    ```sh
    docker build -t splinterpg/splinter-db:1.0 webapp/database
    docker build -t splinterpg/splinter-frontend:1.0 webapp/frontend
    docker build -t splinterpg/splinter-exam-storage:1.0 exam_storage
    docker build -t splinterpg/splinter-inference-engine:1.0 inference_engine
    ```
   You can add --push at the end of each command if you have Docker Buildx, otherwise, push the images manually.

3. **Push the Docker Images to Docker Hub**

    Push the images to Docker Hub:
    ```sh
    docker push splinterpg/splinter-db:1.0
    docker push splinterpg/splinter-frontend:1.0
    docker push splinterpg/splinter-exam-storage:1.0
    docker push splinterpg/splinter-inference-engine:1.0
    ```
    After pushing, check the repository on Docker Hub to ensure the images are available.
4. **Modify Docker Configuration**

    Modify the `docker-compose-prod.yml` file to pull the images from your Docker Hub repository. Replace the image names with the ones you pushed to Docker Hub.

5. **Test Deployment**

    Test the deployment by running the `docker-compose-prod.yml` file:
    ```sh
    docker-compose -f docker-compose-prod.yml pull
    docker-compose -f docker-compose-prod.yml up -d
    ```
    This will pull the latest images and run the containers in the background`.`

**Login Credentials**
* **Email:** splinter.pg@protonmail.com
* **Username:** splinterpg
* **Password:** Can be retrieved from Jan Cychnerski

## Known Issues

- **Issue: `exec /docker-entrypoint.sh: no such file or directory` after running the Docker containers**

    For detailed troubleshooting steps and solution, refer to this [Stack Overflow post](https://stackoverflow.com/questions/38905135/why-wont-my-docker-entrypoint-sh-execute).

- **Unresolved References in IDE:**
    
    If you encounter unresolved references in your IDE (like PyCharm), follow these steps to resolve the issue:
    1. Open PyCharm and navigate to `File -> Settings -> Project:Splinter -> Project Structure`.
    2. Locate the `inference_engine` module within your project structure.
    3. Mark `inference_engine` as `Sources root`
    
    This action informs PyCharm that the `inference_engine` module should be recognized as a source directory, resolving unresolved references and enabling proper module imports within your project.