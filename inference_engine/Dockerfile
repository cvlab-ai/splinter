FROM python:3.10
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . .
ENTRYPOINT gunicorn --workers=4 -b 0.0.0.0:8000 app:app