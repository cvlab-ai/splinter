FROM python:3.10
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . .
CMD ['uvicorn', 'app.app:app', '--host', '0.0.0.0', '--port', '8000']