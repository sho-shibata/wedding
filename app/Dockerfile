FROM python:3.10
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /copy/

# RUN apt-get install -y cron
# RUN echo '* * * * * root /aggreagte/start.sh' > /etc/cron.d/aggreagte
# CMD ['cron', '-f']

# コンテナイメージ内で必要なパッケージをインストール
# RUN apk add --no-cache build-base \
# && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
# && apk del build-base
