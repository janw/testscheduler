FROM node:12 as frontend

WORKDIR /src
COPY frontend ./

RUN \
    yarn --cwd frontend \
    install \
    --prod \
    --no-node-version-check \
    --frozen-lockfile && \
    yarn --cwd frontend run build

FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app
COPY --from=frontend /src/dist ./frontend/dist
COPY testscheduler ./testscheduler
COPY tests ./tests

ENTRYPOINT [ "gunicorn", "testscheduler.wsgi:app", "-b", "0.0.0.0:8000", "--worker-class", "eventlet", "-w", "1" ]
