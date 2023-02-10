FROM php:8.1-fpm

RUN apt-get update \
    && apt-get install -y --no-install-recommends  libpq-dev libpq5 sendmail \
    && docker-php-ext-install pgsql pdo pdo_pgsql shmop \
    && apt-get purge -y --auto-remove libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /www/app

WORKDIR /www/app
COPY ./PHP ./
COPY ./php.ini /usr/local/etc/php/

RUN mkdir /docker-entrypoint.d
COPY entrypoint/docker-entrypoint.sh /
COPY entrypoint/10-setup-sendmail.sh /docker-entrypoint.d
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 8000

CMD ["php", "-S", "0.0.0.0:8000", "-t", "/www/app/"]
