FROM python:3-alpine
#AS builder
ADD . /app 
WORKDIR /app

# Installing dependency directly in 
# the app directory

# RUN pip install --target=/app pydantic pytest requests
RUN pip install -r requirements.txt

# Let's use a distroless container image for 
# ptrhon and some basic SSL certificates
# https://github.com/GoogleContainerTools/distroless

# FROM gcr.io/distroless/python3-debian12
RUN apk update && apk add --no-cache git
# COPY --from=builder /app /app 
# WORKDIR /app 
ENV PYTHONPATH /app 
CMD ["python","main.py"]