FROM nginx:stable
RUN apt-get update && apt-get install -y nginx-extras libnginx-mod-http-dav-ext apache2-utils
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /www/data/splinter && chmod -R 777 /www/data/splinter
RUN mkdir -p /www/data/uploads && chmod -R 777 /www/data/uploads

ARG splinter_user=splinter
ARG splinter_pass=1234

ARG webdav_user=exam_checker
ARG webdav_pass=1234

RUN mkdir -p /etc/apache2/
RUN htpasswd -b -c /etc/apache2/.htpasswd_splinter ${splinter_user} ${splinter_pass}
RUN htpasswd -b -c /etc/apache2/.htpasswd_webdav ${webdav_user} ${webdav_pass}
