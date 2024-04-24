# Interface Engine

## Prerequisites
- Python 3.9
- [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) must be installed and added to your system's PATH to use `pdf2image`.

Before running the Interface Engine, ensure that Python 3.9 is installed on your system. Additionally, for the `pdf2image` library to function correctly, Poppler needs to be installed and accessible via your system's PATH environment variable. You can download and install Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/). This dependency allows for PDF processing within the interface.

## Local Development Setup
To run the Inference Engine locally for development, follow these steps:

1. Clone the repository to your local machine
2. Set up a virtual environment using Python 3.9
3. Install the required Python packages using pip:
    ```bash
    pip install -r requirements.txt
    ```
4. Ensure that Poppler is installed and added to your system's PATH.
5. Build and run the Docker Compose configuration to start the services. This will provide access to `splinter-exam-storage`:
    ```bash
    docker-compose up --build -d
    ```
6. In the config.yaml file, under the exam_storage section, comment out the url parameter and uncomment the `exam_storage_user` and `exam_storage_password` parameters:
    ```yaml
    exam_storage:
      # url: http://splinter-exam-storage
      port: 81
      ...
      exam_storage_user : splinter
      exam_storage_password : 1234
    ```
   **TODO:** Update configuration to read settings from `.env` file.
7. Run the main script from terminal `python main.py` or from PyCharm.
