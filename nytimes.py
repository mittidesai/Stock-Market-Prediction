# SOURCES
#http://docs.python-requests.org/en/latest/user/quickstart/

# IMPORTS
import requests
import csv
#from kafka import KafkaProducer
#from kafka.errors import KafkaError

# CONSTANTS
TIMEOUT = 10
COMPANIES = ["Apple", "Amazon", "Facebook", "Google", "Microsoft"]
SOURCES = ["snippet", "lead_paragraph", "abstract"]
NUM = {company: 0 for company in COMPANIES}
KAFKA_TOPIC = 'keywords'
KAFKA_GROUP = 'my-group'
KAFKA_PORT = 'localhost:9092'

# FUNCTIONS
def getArticles(year="2016", month="1"):
  response = requests.get(
    url = 'https://api.nytimes.com/svc/archive/v1/' + year + '/' + month + '.json',
    params={'api-key': "a4540a0d39de41b88910bb26161e97c6"},
    timeout=TIMEOUT
  )
  responseDict = response.json()
  articles = responseDict["response"]["docs"]
  return articles

def summarize(article):
  summary = { "text" : getText() }
  return summary

def getText():
  text = ""
  for source in SOURCES:
    if article[source] is not None:
      text = text + " " + article[source].encode('utf-8')
  return text

def output(summaries,outputfilename):
  print "Total # of Articles: " + str(len(summaries))
  print NUM
  writeToCSV(summaries, outputfilename)
  #sendToKafka(summaries)

def writeToCSV(summaries, outputfilename):
  with open(outputfilename, 'wb') as outputFile:
    writer = csv.DictWriter(outputFile, fieldnames = summaries[0].keys())
    writer.writeheader()
    writer.writerows(summaries)
  print "Data has been exported to " + outputfilename

def sendToKafka(summaries):
  producer = KafkaProducer(bootstrap_servers=[KAFKA_PORT])
  for summary in summaries:
    key = str(summary["text"])
    values = ' '.join([str(summary[company]) for company in COMPANIES]).encode("utf-8", errors='ignore')
    future = producer.send(KAFKA_TOPIC, key=key, value=values)

# MAIN METHOD
if __name__ == "__main__":
    year = '2012'
    for month in range(1,13):
        outputfilename = str(month) + "_" + year +".csv"
        print outputfilename
        articles = getArticles(year='2012',month=str(month))
        summaries = [summarize(article) for article in articles]
        output(summaries, outputfilename)
