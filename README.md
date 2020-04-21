# Test Scheduler Application

## Quick Start

The application is packaged using Docker. Using [Docker-compose](https://docs.docker.com/compose/install/), all components can be spun up quickly and will run completely containerized. With the included `docker-compose.yml` the application frontend is available at <http://localhost:8000>:

```bash
docker-compose up
```

Alternatively you may use `make up` to bring the application up. The (Postgres) database is stored in a docker volume, therefore keeping state between executions.

Run `make build` to trigger new build of the Docker image. Please note that the image is tagged as `janwh/testscheduler` but it is not publicly available on Docker Hub.

## Development setup

Development requires `make`, NodeJS (with `yarn`), and `python3` (3.6+) to be installed. Two options are available to start up a development instance of the application:

**Option 1:**

1. Run `make deps` to install dependencies. If you do not have the desired version of Python in your PATH by default, you may provide a binary by calling `PYTHON=/my/custom/python make deps` instead (defaults to `python3`).
1. Run `make serve` to start a Webpack Dev Server, a dev instance of the test scheduler, and an RQ background worker. Components are run by [honcho](https://honcho.readthedocs.io) in parallel.

**Option 2:**

1. First install all requirements for frontend and backend:

    1. Setup a python virtualenv and install requirements

        ```bash
        python -m venv .venv
        . ./.venv/bin/activate
        pip install -r requirements.txt -r requirements-dev.txt
        ```

    1. Install the frontend dependencies

        ```bash
        yarn --cwd ./frontend install
        ```

1. Now to run all components, there are three steps required in separate terminal sessions:

   1. Run an instance of the web backend:

       ```bash
       . ./.venv/bin/activate
       python -m testscheduler
       ```

   1. Run an instance of the frontend dev server:

       ```bash
       yarn --cwd ./frontend run serve
       ```

   1. Run an instance of the RQ background worker

       ```bash
       . ./.venv/bin/activate
       rq worker
       ```

## Running the application testsuite

The *actual* tests for the backend are included in the `./tests/backend` directory, next to dummy tests for the application. Since the dummy tests include failing ones, to test the application test selection should be set to the `./tests/backend` directory.

A convenient wrapper for running the testsuite is available with `make test`.

The testsuite is also available via the frontend to be run via the runner worker.
