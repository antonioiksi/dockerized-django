FROM python:3.6-slim-jessie

# init
RUN mkdir /www
WORKDIR /www
COPY requirements.txt /www/

# setup
# RUN apt-get update -y
# RUN apt-get upgrade -y
# RUN apt-get install -y postgresql-client
# RUN apt-get install -y \
#     postgresql-client \
#     postgresql-dev
# RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# clean
# RUN apk del -r python3-dev postgresql

# prep
ENV PYTHONUNBUFFERED 1
COPY . /www/