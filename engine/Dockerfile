FROM debian:stable-20220316

RUN apt-get update && apt-get -y install \
    python3 \
    python3-pip \
    libpq-dev

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN useradd -ms /bin/bash splinter
USER splinter
WORKDIR /home/splinter
COPY ./src/ .

CMD ["python3", "./main.py"]
