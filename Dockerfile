FROM python:3.7

# 바로 수정할 수 있게 vim 설치
RUN apt-get -y update
RUN apt-get -y install vim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update
RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev

COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app
RUN pip install -r requirements.txt

COPY . /usr/src/app