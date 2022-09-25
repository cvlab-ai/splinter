FROM php:8.0-rc-cli

RUN useradd -ms /bin/bash splinter

WORKDIR /home/splinter
COPY ./PHP ./app

EXPOSE 8000

ENTRYPOINT ["php", "-S", "0.0.0.0:8000", "-t", "/home/splinter/app/"]
