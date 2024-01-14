FROM keitarodxs/aia:aia-utils_0.1.8
WORKDIR /app

RUN apt-get update && apt-get -y install
RUN apt-get install graphviz
RUN pip install --upgrade pip

RUN pip install poetry
COPY . .
COPY pyproject.toml poetry.lock ./
RUN poetry install

CMD [ "poetry", "run", "daemon"]
