FROM thehale/python-poetry:1.7.1-py3.11-slim

COPY pyproject.toml poetry.lock ./

WORKDIR /app

COPY . .

RUN poetry install

CMD [ "poetry", "run", "daemon"]