FROM python:3.10-slim



RUN apt update && \
    apt install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip
WORKDIR /code 
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt




COPY ./src src
COPY --chown=nonroot:nonroot alembic/ alembic/
COPY --chown=nonroot:nonroot alembic.ini .
COPY --chown=nonroot:nonroot entrypoint.sh .

CMD ["./entrypoint.sh"]

