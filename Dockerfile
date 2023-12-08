FROM python:3-slim
COPY . /app
RUN pip install pydantic jinja2

CMD python3 -u /app/main.py \
    /github/workspace/$INPUT_DATAPATH \
    /app/templates \
    /app/assets \
    /github/workspace/$INPUT_SITEPATH \
    $INPUT_BASEURL
