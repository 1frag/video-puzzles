FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app/src

RUN mkdir -p /app/src
WORKDIR /app

RUN pip install -U pip wheel setuptools

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY run_api.py /app/src
COPY .env /app/src
COPY api /app/src/api

EXPOSE 8000

CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "run_api:app", "-b", "0.0.0.0:8000", "--disable-redirect-access-to-syslog", "--forwarded-allow-ips=\"*\""]
