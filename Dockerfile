FROM python:3.7.4-buster as pdf-pii-remover

ENV PYTHONDONTWRITEBYTECODE=1
ARG PII_HOME=/home/rihan/pdf-pii-remover
WORKDIR $PII_HOME

RUN apt-get update \
&& apt-get -y install build-essential libpoppler-cpp-dev pkg-config python3-dev \
&& mkdir -p output \
&& rm -rf /var/lib/apt/lists/* \
&& useradd --create-home --shell /bin/bash rihan \
&& chown -R rihan:rihan $PII_HOME

# files necessary to build the project
COPY requirements.txt ./
COPY pii.py ./
COPY main.py ./

RUN pip3 install -r requirements.txt

COPY input/ input/

VOLUME ["/home/rihan/pdf-pii-remover/output"]
ENTRYPOINT ["python3", "/home/rihan/pdf-pii-remover/main.py"]
