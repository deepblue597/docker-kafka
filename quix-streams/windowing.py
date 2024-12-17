from datetime import timedelta
from quixstreams import Application
from quixstreams.models import TopicConfig

app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="windowing_events",
)

# Define the Kafka topics
wikipedia_topic = app.topic("wikipedia-events", value_deserializer="json")
windowing = app.topic("windowing", value_serializer="json")

sdf = app.dataframe(topic=wikipedia_topic)
sdf['len_diff'] = sdf['new_length'] - sdf['old_length']
sdf = (
    # Extract "temperature" value from the message

    sdf.apply(lambda event: event["len_diff"])

    # Define a tumbling window of 1 hour
    # You can also pass duration_ms as an integer of milliseconds
    .tumbling_window(duration_ms=timedelta(seconds=10))

    # Specify the "mean" aggregate function
    .mean()

    # Emit updates for each incoming message
    .current()

    # Unwrap the aggregated result to match the expected output format
    .apply(
        lambda result: {
            "avg_len_diff": result["value"],
            "window_start_ms": result["start"],
            "window_end_ms": result["end"],
        }
    )
)

sdf = sdf.to_topic(windowing)
# Run the streaming application (app automatically tracks the sdf!)
app.run()
