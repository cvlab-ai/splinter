FROM node:latest

RUN useradd -ms /bin/bash splinter

WORKDIR /home/splinter
COPY ./ ./app

WORKDIR /home/splinter/app
RUN npm install

EXPOSE 4200
ENTRYPOINT ["node_modules/.bin/ng", "serve", "--host", "0.0.0.0", "--disable-host-check"]
