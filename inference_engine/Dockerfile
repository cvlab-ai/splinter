FROM python:3.9

RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
