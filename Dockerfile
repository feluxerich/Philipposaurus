FROM python:3.8.0-slim

WORKDIR /philipposaurus

COPY . /philipposaurus

RUN apt upgrade

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY errors.py /philipposaurus
COPY main.py /philipposaurus
COPY utils.py /philipposaurus

EXPOSE 1337:1337

RUN python /philipposaurus/main.py
