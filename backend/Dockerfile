FROM python:3.11-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod 755 /app/entrypoint.sh

COPY . .
ENTRYPOINT ["/app/entrypoint.sh"]