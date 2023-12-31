FROM python:3.11-slim
COPY . /app

WORKDIR /app

RUN apt-get update
RUN pip install .

ENV PYTHONPATH="${PYTHONPATH}:/app/"
CMD ["python", "-m", "src"]
