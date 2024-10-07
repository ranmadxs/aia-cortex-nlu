FROM keitarodxs/aia-utils:latest

WORKDIR /app

RUN apt-get update && apt-get -y install
RUN apt-get install graphviz -y
RUN apt-get install libhdf5-dev -y
RUN pip install --upgrade pip

RUN pip install poetry
COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install

CMD [ "poetry", "run", "daemon"]
