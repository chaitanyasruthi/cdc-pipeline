FROM python:3.10

WORKDIR /app

COPY processor.py .

RUN pip install kafka-python pandas pyarrow

CMD ["python", "processor.py"]