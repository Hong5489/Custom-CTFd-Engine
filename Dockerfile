FROM python:3.7-slim-buster
WORKDIR /opt/CTFd
RUN mkdir -p /opt/CTFd /var/log/CTFd /var/uploads

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y  \
        build-essential \
        default-mysql-client \
        python-dev \
        libffi-dev \
        libssl-dev \
        git\
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common

RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -\
    && add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/debian \
       $(lsb_release -cs) \
       stable"\
    && apt-get update\
    && apt-get install -y docker-ce\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

COPY . /opt/CTFd

RUN pip install -r requirements.txt --no-cache-dir
# hadolint ignore=SC2086
RUN for d in CTFd/plugins/*; do \
        if [ -f "$d/requirements.txt" ]; then \
            pip install -r $d/requirements.txt --no-cache-dir; \
        fi; \
    done;

RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    ctfd
#RUN chmod +x /opt/CTFd/docker-entrypoint.sh \
#    && chown -R 1001:1001 /opt/CTFd /var/log/CTFd /var/uploads

#USER 1001
EXPOSE 8000
ENTRYPOINT ["/opt/CTFd/docker-entrypoint.sh"]
