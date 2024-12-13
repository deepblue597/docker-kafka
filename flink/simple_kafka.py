from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink
from pyflink.common import Types, WatermarkStrategy
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaRecordSerializationSchema
from pyflink.datastream import stream_execution_environment


def main():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()

    # env.add_jars(
    #     "file:///opt/flink/flink-sql-connector-kafka-1.15.4.jar")

    # Kafka Source Configuration
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:39092")  \
        .set_topics("wikipedia-events")  \
        .set_group_id("flink-consumer-group")  \
        .set_value_only_deserializer(SimpleStringSchema())  \
        .build()

    record_serializer = KafkaRecordSerializationSchema.builder() \
        .set_topic("test-topic") \
        .set_value_serialization_schema(SimpleStringSchema()) \
        .build()

    # Kafka Sink Configuration
    kafka_sink = KafkaSink.builder() \
        .set_bootstrap_servers("localhost:39092") \
        .set_record_serializer(record_serializer) \
        .build()

    # Add the Kafka source to the environment

    stream = env.from_source(kafka_source, WatermarkStrategy.no_watermarks(
    ), "Kafka Source")  # env.from_source(kafka_source, Types.STRING())

    # Process the stream (you can apply transformations here)
    processed_stream = stream.map(lambda x: x, output_type=Types.STRING())

    # Add the Kafka sink to the environment
    processed_stream.sink_to(kafka_sink)

    # Execute the Flink job
    env.execute("Simple Kafka Flink Job")


if __name__ == "__main__":
    main()
