FROM python:3.8-slim
RUN pip3 install flask pyop gunicorn
COPY . /app
WORKDIR /app
ENTRYPOINT ["./gunicorn_starter.sh"]
