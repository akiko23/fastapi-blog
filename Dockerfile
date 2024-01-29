FROM python:3.11-slim
COPY . /app

WORKDIR /app

RUN apt-get update
RUN pip install .

CMD ["python", "-m", "src.fastapi_blog"]
