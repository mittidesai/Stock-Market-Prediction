#	DOCUMENTATION	#
#		How to execute:
#			spark-submit ml.py
#		Data Format in Kafka:
#			Key: y value
#			Value: x values (space-separated)
#			Example:
#				y = 1.0		x = 1.0 2.0 3.0


#	SOURCES		#
#		https://spark.apache.org/docs/1.6.2/api/python/pyspark.sql.html
#		http://spark.apache.org/docs/1.6.1/api/python/pyspark.ml.html
#		https://spark.apache.org/docs/1.6.1/ml-classification-regression.html
#		spark.apache.org/docs/1.6.1/ml-guide.html


#	IMPORTS		#
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.mllib.linalg import Vectors
from pyspark.ml.regression import LinearRegression, DecisionTreeRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from kafka import KafkaConsumer
from random import shuffle
import os


#	CONSTANTS	#
sc = SparkContext("local", "ml", pyFiles=['ml.py'])
sqlContext = SQLContext(sc)
KAFKA_TOPIC = 'my-topic'
KAFKA_GROUP = 'my-group'
KAFKA_PORT = 'localhost:9092'


#	FUNCTIONS	#
def kafkaStream(topic, group = KAFKA_GROUP, port = KAFKA_PORT):
	return 	KafkaConsumer(topic,
			group_id=group,
			bootstrap_servers=[port])

# returns a List of (y, x) Tuples, where x is a Vector
def getFromTopic(topic):
	# Actual Data streamed from Kafka:
	data = []
	for message in kafkaStream(topic=topic):
		if message.key == "END":
			break
		y = message.key
		x = Vectors.dense(message.value.split(" "))
		data_point = (y, x)
		data.extend(data_point)

	# Sample Data: use for testing purposes
	# data = [
	# (1.0, Vectors.dense(2.0)),
	# (9.0, Vectors.dense(3.0)),
	# (3.0, Vectors.dense(4.0)),
	# (2.0, Vectors.dense(5.0)),
	# (5.0, Vectors.dense(6.0)),
	# (4.0, Vectors.dense(1.0)),
	# (7.0, Vectors.dense(4.5)),
	# (8.0, Vectors.dense(5.5)),
	# ]

	return data

def toDataFrame(data):
	return sqlContext.createDataFrame(data, ["y", "x"])

def trainLRmodel(training_df):
	return LinearRegression(featuresCol="x", labelCol="y", predictionCol="prediction").fit(training_df)

def trainDTmodel(training_df):
	return DecisionTreeRegressor(featuresCol="x", labelCol="y", predictionCol="prediction").fit(training_df)

def test_single_split(model):
	(training_df, testing_df) = data.randomSplit([0.75, 0.25])
	lr_model = trainLRmodel(training_df)
	dt_model = trainDTmodel(training_df)
	print "The Root-Mean-Square-Error of the Linear Regression Model is " + str(root_mean_square_error(model, testing_df))
	print "The Root-Mean-Square-Error of the Decision Tree Model is " + str(root_mean_square_error(model, testing_df))

def createPartitions(df, numPartitions=3):
	rows = df.collect()
	shuffle(df.collect())
	numRows = len(rows)
	partitionSize = numRows / numPartitions
	partitions = []
	for i in range(numPartitions):
		start = i*partitionSize
		end = (i+1)*partitionSize
		partition = toDataFrame(rows[start:end])
		partitions.append(partition)
	return partitions

def mergeTrainingPartitions(partitions, testing_df):
	training_df = []
	for partition in partitions:
		if partition is not testing_df:
			if not training_df:
				training_df = partition
			else:
				training_df.unionAll(partition)
	return training_df

def test_cross_validation(data, n=3):
	partitions = createPartitions(data, n)
	lr_rmse = []
	dt_rmse = []
	for testing_df in partitions:
		training_df = mergeTrainingPartitions(partitions, testing_df)
		lr_model = trainLRmodel(training_df)
		dt_model = trainDTmodel(training_df)
		lr_rmse.append(root_mean_square_error(lr_model, testing_df))
		dt_rmse.append(root_mean_square_error(dt_model, testing_df))
	print "The Root-Mean-Square-Errors of the Linear Regression Models are " + " ".join(map(str, lr_rmse))
	print "The Root-Mean-Square-Errors of the Decision Tree Models are " + " ".join(map(str, dt_rmse))

def root_mean_square_error(model, testing_df):
	predictions = model.transform(testing_df)
	evaluator = RegressionEvaluator(labelCol="y", predictionCol="prediction", metricName="rmse")
	rmse = evaluator.evaluate(predictions)
	return rmse


#	MAIN METHOD	#
if __name__ == "__main__":
	data = toDataFrame(getFromTopic(KAFKA_TOPIC))
	test_cross_validation(data)
