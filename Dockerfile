FROM python:3.12-slim

WORKDIR /app/py-conf-mcp

COPY requirements.build.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir \
    -r requirements.build.txt

COPY requirements.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir \
    -r requirements.txt

COPY requirements.dev.txt ./
RUN pip install --disable-pip-version-check --no-cache-dir \
    -r requirements.txt \
    -r requirements.dev.txt

COPY py_conf_mcp ./py_conf_mcp
COPY config ./config

COPY tests ./tests
COPY setup.cfg pyproject.toml ./

ENV CONFIG_FILE=./config/server.yaml

CMD ["python3", "-m", "py_conf_mcp", "--transport=sse", "--host=0.0.0.0", "--port=8080"]
