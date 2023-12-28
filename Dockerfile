FROM python:3.11.7
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry

COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install

CMD [ "poetry", "run", "daemon"]
