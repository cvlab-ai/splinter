FROM nginx:stable
RUN apt-get update && apt-get install -y nginx-extras libnginx-mod-http-dav-ext
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /www/data
RUN chmod -R 777 /www/data
