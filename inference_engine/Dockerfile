FROM python:3.9

RUN apt-get update && apt-get install -y python3-opencv poppler-utils
RUN pip install --upgrade pip

WORKDIR /app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
