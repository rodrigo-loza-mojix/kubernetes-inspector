FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1
COPY requirements.txt /
RUN pip install -r requirements.txt &&\
    rm requirements.txt

