FROM postgres:12.10

RUN useradd -ms /bin/bash splinter

WORKDIR /home/splinter
COPY db.init / ./
