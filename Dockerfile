FROM python:3.13-alpine

WORKDIR /app
COPY . .

RUN apk update \
 && apk add \
    python3-dev


RUN pip install -r conf/requirements.txt -c conf/constraints.txt

CMD ["python", "consumer.py"]

WORKDIR /app/src
