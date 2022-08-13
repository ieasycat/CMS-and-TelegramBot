FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /hr_bot-master

COPY requirements.txt /hr_bot-master
COPY boot.sh .
RUN pip3 install --upgrade pip -r requirements.txt
RUN chmod +x boot.sh

COPY ./ .

RUN chmod +x /hr_bot-master/boot.sh