from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction

# Create an execution environment
env = StreamExecutionEnvironment.get_execution_environment()

# Define the data source (in this case, a list)
data = env.from_collection(collection=["hello", "world", "flink"])

# Define a simple MapFunction to transform the data


class MyMapFunction(MapFunction):
    def map(self, value):
        return value.upper()


# Apply the transformation
result = data.map(MyMapFunction())

# Print the result
result.print()

# Execute the Flink job
env.execute("PyFlink Example")
