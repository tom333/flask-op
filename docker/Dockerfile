FROM python:3.8-slim

RUN pip3 install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install
COPY . /app
COPY docker/config.py /app/flask_op/
COPY docker/gunicorn_starter.sh .
ENTRYPOINT ["./gunicorn_starter.sh"]
