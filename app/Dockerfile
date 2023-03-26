FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /copy/

