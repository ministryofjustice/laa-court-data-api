FROM python:3.10-alpine

WORKDIR /code

RUN apk --update-cache upgrade \
&& apk --no-cache add --upgrade gcc \
    musl-dev \
    build-base \
    expat \
    'libretls>=3.3.4-r3'

COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock
COPY ./logging.conf /code/logging.conf
COPY ./laa_court_data_api_app /code/laa_court_data_api_app

RUN pip install --upgrade pip pipenv

RUN PIPENV_PIPFILE="/code/Pipfile" pipenv install --system --deploy

RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser
RUN chown -R appuser:appuser /code
USER 1001

ARG COMMIT_ID
ARG BUILD_DATE
ARG BUILD_TAG
ARG APP_BRANCH
ENV COMMIT_ID=${COMMIT_ID}
ENV BUILD_DATE=${BUILD_DATE}
ENV BUILD_TAG=${BUILD_TAG}
ENV APP_BRANCH=${APP_BRANCH}

EXPOSE 80
CMD ["uvicorn", "laa_court_data_api_app.main:app", "--host", "0.0.0.0", "--port", "80"]