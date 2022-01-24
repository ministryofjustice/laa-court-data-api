FROM python:3.10-alpine

WORKDIR /code

RUN apk add gcc \
    musl-dev \
    build-base

COPY ./requirements.txt /code/requirements.txt
COPY ./laa_court_data_api_app /code/laa_court_data_api_app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser
RUN chown -R appuser:appuser /code
USER appuser

EXPOSE 80
CMD ["uvicorn", "laa_court_data_api_app.main:app", "--host", "0.0.0.0", "--port", "80"]