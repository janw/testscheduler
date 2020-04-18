FROM node:12 as frontend

WORKDIR /src
COPY frontend ./

RUN yarn install --non-interactive --prod && yarn run build

FROM python:3.7

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /app
COPY --from=frontend /src/dist ./frontend/dist
COPY testscheduler ./testscheduler

ENTRYPOINT [ "gunicorn", "testscheduler", "-b", "0.0.0.0:8000" ]
