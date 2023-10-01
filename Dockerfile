FROM python:3-slim AS builder
ADD . /app 
WORKDIR /app

# Installing dependency directly in 
# the app directory
RUN pip install --target=/app pydantic pytest

# Let's use a distroless container image for 
# ptrhon and some basic SSL certificates
# https://github.com/GoogleContainerTools/distroless

FROM gcr.io/distroless/python3-debian12
COPY --from=builder /app /app 
# WORKDIR /app 
ENV PYTHONPATH /app 
CMD ["/app/main.py"]