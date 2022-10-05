FROM php:8.1-fpm

RUN apt-get update
RUN apt-get update \
    && apt-get install -y --no-install-recommends  libpq-dev libpq5 \
    && docker-php-ext-install pgsql pdo pdo_pgsql shmop \
    && apt-get purge -y --auto-remove libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash splinter

WORKDIR /home/splinter
COPY ./PHP ./app
COPY ./php.ini /usr/local/etc/php/

EXPOSE 8000

ENTRYPOINT ["php", "-S", "0.0.0.0:8000", "-t", "/home/splinter/app/"]
