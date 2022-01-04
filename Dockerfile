FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -y software-properties-common \ 
  build-essential checkinstall \
  libmysqlclient-dev \
  mysql-client \
  build-essential \
  git \
  nginx \
  libgdal-dev \ 
  supervisor \
  sqlite3 \
  locales && \
  rm -rf /var/lib/apt/lists/*

# install python3.9
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3.9-distutils \
  python3.9 \
  python3-dev \
  python3-pip \
  libpython3.9-dev

RUN python3.9 -m pip install -U pip setuptools

ADD requirements/requirements.txt /project/

WORKDIR /project

RUN python3.9 -m pip install -r /project/requirements.txt

ADD . /project/


ENV SERVICE_SERVER_DOMAIN_OR_IP=${SERVICE_SERVER_DOMAIN_OR_IP}

ENV DATABASE_ENGINE=${DATABASE_ENGINE} \
  DATABASE_HOST=${DATABASE_HOST} \
  DATABASE_PORT=${DATABASE_PORT} \
  DATABASE_NAME=${DATABASE_NAME} \
  DATABASE_USER=${DATABASE_USER} \
  DATABASE_PASSWORD=${DATABASE_PASSWORD} \
  DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY} \
  DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} \
  SECRET_KEY=${SECRET_KEY}} \
  ALGORITHM=${ALGORITHM} \
  YOUTUBE_DATA_API_KEY=${YOUTUBE_DATA_API_KEY} \
  EMAIL_HOST=${EMAIL_HOST} \
  EMAIL_PORT=${EMAIL_PORT} \
  EMAIL_HOST_USER=${EMAIL_HOST_USER} \
  EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD} \
  AWS_IAM_ACCESS_KEY=${AWS_IAM_ACCESS_KEY} \
  AWS_IAM_SECRET_KEY=${AWS_IAM_SECRET_KEY} \
  AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME} \
  AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}} \
  CACHES_BACKEND=$CACHES_BACKEND \
  CACHES_KEY_PREFIX={CACHES_KEY_PREFIX} \
  CACHES_LOCATION=${CACHES_LOCATION}


RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisor.conf /etc/supervisor/conf.d/

EXPOSE 80
EXPOSE 443

CMD ["supervisord", "-n"]
