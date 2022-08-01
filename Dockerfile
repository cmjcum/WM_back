FROM python:3.7.5-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y cmake libgl1-mesa-glx
RUN python -m pip install --upgrade pip
COPY requirements.txt /usr/src/app/

WORKDIR /usr/src/app
RUN pip install tensorflow==2.9.0
RUN pip install torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

COPY . /usr/src/app