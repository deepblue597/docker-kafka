# Use the Flink 1.20 base image
FROM flink:1.20.0

# Install Python dependencies
RUN apt-get update -y && \
    apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libffi-dev wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python 3.11
RUN wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz && \
    tar -xvf Python-3.11.6.tgz && \
    cd Python-3.11.6 && \
    ./configure --enable-shared && \
    make -j6 && \
    make install && \
    ldconfig /usr/local/lib && \
    cd .. && rm -f Python-3.11.6.tgz && rm -rf Python-3.11.6 && \
    ln -s /usr/local/bin/python3 /usr/local/bin/python

# Install the latest PyFlink
RUN pip3 install apache-flink

# Add the correct Kafka connector JAR for Flink 1.20
ADD https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.4.0-1.20/flink-sql-connector-kafka-3.4.0-1.20.jar /opt/flink/lib/

# # Clean up unnecessary files to reduce image size
# RUN apt-get clean && \
#     rm -rf /var/lib/apt/lists/* /tmp/*
