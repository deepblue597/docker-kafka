FROM apache/flink:1.15-scala_2.12

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

#COPY src/simple_kafka.py /app/simple_kafka.py

#WORKDIR /app

#CMD ["python", "simple_kafka.py"]