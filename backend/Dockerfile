FROM python:3.12-slim

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
    # Python configuration:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

WORKDIR /app

COPY /backend/requirements.txt .
COPY /backend/entrypoint.sh .

RUN apt-get update && \
    pip install --upgrade pip &&\
    pip install -r requirements.txt --no-cache-dir

COPY /backend/ .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
