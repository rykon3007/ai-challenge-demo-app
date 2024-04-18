FROM python:3.10
USER root

RUN apt-get update && \
    apt-get -y install --reinstall ca-certificates && \
    apt-get -y install software-properties-common && \
    pip install --upgrade pip

# requirements.txtファイルをコンテナにコピー
COPY requirements.txt /tmp/

# requirements.txtにリストされたパッケージをインストール
RUN pip install -r /tmp/requirements.txt