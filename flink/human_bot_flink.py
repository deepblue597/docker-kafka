from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaSink
import json
from pyflink.table import TableEnvironment, EnvironmentSettings
from pyflink.datastream import stream_execution_environment


def parse_event(json_string):
    """Parse Kafka JSON string into a Python dictionary."""
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return None  # Return None or handle error as appropriate


if __name__ == "__main__":
    # Initialize the Flink environment
    env = StreamExecutionEnvironment.get_execution_environment()

    env.add_jars("file:///jars/flink-sql-connector-kafka-3.0.1-1.18.jar")

    # Kafka source configuration (input topic)
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("localhost:39092") \
        .set_topics("wikipedia-events") \
        .set_group_id("flink-consumer-group") \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    # Kafka sink configurations (output topics)
    bot_sink = KafkaSink.builder() \
        .set_bootstrap_servers("localhost:39092") \
        .set_record_serializer(SimpleStringSchema()) \
        .set_topics("bot-edits") \
        .build()

    human_sink = KafkaSink.builder() \
        .set_bootstrap_servers("localhost:39092") \
        .set_record_serializer(SimpleStringSchema()) \
        .set_topics("human-edits") \
        .build()

    # Create a stream from the Kafka source
    data_stream = env.from_source(
        kafka_source, watermark_strategy=None, source_name="KafkaSource")

    # Parse the incoming JSON events
    parsed_stream = data_stream.map(parse_event)

    # Filter out any None values from malformed events
    parsed_stream = parsed_stream.filter(lambda event: event is not None)

    # Filter events into bot and human streams
    bot_edits = parsed_stream.filter(
        lambda event: event.get('user_type') == 'bot')
    human_edits = parsed_stream.filter(
        lambda event: event.get('user_type') == 'human')

    # Write filtered streams to separate Kafka topics
    bot_edits.sink_to(bot_sink)
    human_edits.sink_to(human_sink)

    # Execute the Flink pipeline
    env.execute("Separate Bot and Human Edits")
