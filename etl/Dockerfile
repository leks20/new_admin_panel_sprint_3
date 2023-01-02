FROM python:3.10-slim-buster as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8

RUN apt-get clean && apt-get update && \
    apt-get install -y locales libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install virtualenv && \
    locale-gen ru_RU && \
    locale-gen ru_RU.UTF-8 && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt

FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU.UTF-8 \
    LC_ALL=ru_RU.UTF-8 \
    PORT=80

WORKDIR /code

RUN pip install --upgrade pip
COPY --from=builder /code/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY extract ./extract
COPY load ./load
COPY transform ./transform
COPY utils ./utils
COPY __init__.py config.py main.py README.md state.json ./

EXPOSE $PORT

CMD ["./main.py"]
ENTRYPOINT ["python"]
