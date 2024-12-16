env.add_jars(
        "file:///opt/flink/lib/flink-sql-connector-kafka-3.4.0-1.20.jar"
    )

    # Kafka Source Configuration
    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers("broker-1:9092")  \
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
        .set_bootstrap_servers("broker-1:9092") \
        .set_record_serializer(record_serializer) \
        .build()

    # Add the Kafka source to the environment

    stream = env.from_source(kafka_source, WatermarkStrategy.no_watermarks(
    ), "Kafka Source")  # env.from_source(kafka_source, Types.STRING())

    # Process the stream (you can apply transformations here)
    processed_stream = stream.map(lambda x: x, output_type=Types.STRING())

    # Add the Kafka sink to the environment
    processed_stream.sink_to(kafka_sink)