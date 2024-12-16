from quixstreams import Application

# A minimal application reading temperature data in Celsius from the Kafka topic,
# converting it to Fahrenheit and producing alerts to another topic.

# Define an application that will connect to Kafka
app = Application(
    broker_address="localhost:39092",  # Kafka broker address
    auto_offset_reset="earliest",
    consumer_group="product_review_bot_alert",
)

# Define the Kafka topics
wikipedia_topic = app.topic("wikipedia-events", value_deserializer="json")
bot_topic = app.topic("bot-alertsv2", value_serializer="json")

# Create a Streaming DataFrame connected to the input Kafka topic
sdf = app.dataframe(topic=wikipedia_topic)

# Convert temperature to Fahrenheit by transforming the input message (with an anonymous or user-defined function)
sdf = sdf.apply(lambda event: event.get('user_type') == 'bot')

# Filter values above the threshold
# sdf = sdf[sdf["value"] == true]

# Produce alerts to the output topic
sdf = sdf.to_topic(bot_topic)

# Run the streaming application (app automatically tracks the sdf!)
app.run()
