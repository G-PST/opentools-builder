FROM python:3-slim
COPY . /app
RUN pip install pydantic jinja2

CMD python3 -u /app/main.py \
    /github/workspace/$INPUT_DATAPATH \
    /app/templates \
    /app/assets \
    /github/workspace/$INPUT_SITEPATH \
    /github/workspace/$INPUT_ERRORPATH \
    $GITHUB_OUTPUT \
    $INPUT_BASEURL
