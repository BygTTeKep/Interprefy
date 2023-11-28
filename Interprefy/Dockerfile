FROM python:3.11-alpine3.18

WORKDIR /Interprefy

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r requirements.txt

COPY . .

# RUN sudo apt install postgresql postgresql-contrib
# RUN sudo systemctl start postgresql.service
# FROM nginx:mainline-alpine3.18-slim
# RUN rm -rf /usr/share/nginx/html/*

# COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf
# ENTRYPOINT ["nginx", "-g", "daemon off;"]