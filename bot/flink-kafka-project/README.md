# flink-kafka-project documentation

## Overview
This project demonstrates how to utilize Apache Flink with Kafka for streaming data processing. The main script, `simple_kafka.py`, sets up a Kafka source and sink, processes the incoming stream, and defines the necessary configurations for connecting to Kafka.

## Project Structure
```
flink-kafka-project
├── src
│   └── simple_kafka.py      # Python script for Flink and Kafka integration
├── Dockerfile                # Instructions to build the Docker image
├── requirements.txt          # Python dependencies for the project
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd flink-kafka-project
   ```

2. **Install dependencies**:
   You can install the required Python packages using pip. Make sure you have Python and pip installed.
   ```
   pip install -r requirements.txt
   ```

3. **Build the Docker image**:
   To build the Docker image for the project, run the following command in the project root directory:
   ```
   docker build -t flink-kafka-project .
   ```

4. **Run the Docker container**:
   After building the image, you can run the container using:
   ```
   docker run flink-kafka-project
   ```

## Usage
The `simple_kafka.py` script connects to a Kafka broker, consumes messages from the `wikipedia-events` topic, processes them, and sends the results to the `test-topic`. You can modify the script to change the topics or processing logic as needed.

## Contributing
Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.