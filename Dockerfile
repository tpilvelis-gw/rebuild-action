FROM python:3.7-alpine

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh


COPY hello.py /hello.py

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/entrypoint.sh"]