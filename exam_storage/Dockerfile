FROM nginx:stable

ENV NGINX_VERSION 1.18.0

RUN apt-get update && apt-get install -y nginx-extras libnginx-mod-http-dav-ext apache2-utils libpcre3 libpcre3-dev

RUN addgroup --system --gid 101 nginx && \
    adduser --system --disabled-login --ingroup nginx --no-create-home --home /nonexistent --gecos "nginx user" --shell /bin/false --uid 101 nginx && \
    apt-get update && \
    apt-get install -y --no-install-recommends wget gcc g++ libc-dev make ca-certificates libfindbin-libs-perl unzip && \
    mkdir build && cd build && \
    wget https://ftp.icm.edu.pl/packages/zlib/zlib-1.2.11.tar.gz && tar -zxf zlib-1.2.11.tar.gz && \
    cd zlib-1.2.11 && ./configure && make && cd .. && \
    wget https://www.openssl.org/source/old/1.1.1/openssl-1.1.1b.tar.gz && \
    tar -zxf openssl-1.1.1b.tar.gz && cd openssl-1.1.1b && \
    ./config && make && make install && cd .. && \
    wget https://github.com/evanmiller/mod_zip/archive/master.zip && unzip master.zip && \
    wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz && tar -zxf nginx-${NGINX_VERSION}.tar.gz && \
    cd nginx-${NGINX_VERSION} && \
    ./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp \
    --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
    --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module \
    --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module \
    --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module \
    --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module \
    --with-cc-opt='-g -O2 -ffile-prefix-map=/data/builder/debuild/nginx-1.23.1/debian/debuild-base/nginx-1.23.1=. -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' \
    --with-ld-opt='-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie -lpcre' --with-zlib=../zlib-1.2.11 --add-module=../mod_zip-master && \
    make && make install && cd .. && \
    ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/nginx && \
    ln -s /usr/lib/nginx/modules/ /etc/nginx/modules && \
    cd .. && rm -rf build && \
    apt-get remove --purge --auto-remove -y wget gcc g++ libc-dev make ca-certificates libfindbin-libs-perl unzip && rm -rf /var/lib/apt/lists/*

#install python for zip creation script
RUN apt-get update && apt-get install -y python3

################################################################################
RUN mkdir -p /www/data/splinter && chmod -R 777 /www/data/splinter && \
    mkdir -p /www/data/uploads && chmod -R 777 /www/data/uploads && \
    chmod o+w /www/data

COPY nginx.conf /etc/nginx/nginx.conf
COPY ./scripts /www/data/scripts

ARG splinter_user=splinter
ARG splinter_pass=1234
ARG webdav_user=exam_checker
ARG webdav_pass=1234

RUN mkdir -p /etc/apache2/ && \
    htpasswd -b -c /etc/apache2/.htpasswd_splinter ${splinter_user} ${splinter_pass} && \
    htpasswd -b -c /etc/apache2/.htpasswd_webdav ${webdav_user} ${webdav_pass}

################################################################################

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

# rm doubled modules
RUN rm /etc/nginx/modules-enabled/50-mod-mail.conf /etc/nginx/modules-enabled/50-mod-stream.conf && \
    mkdir -p /var/cache/nginx/


EXPOSE 80
STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
