import pika
import json
import os
from minio import Minio
import os
from io import BytesIO
import pandas as pd
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import leaguestandings
# might need scoreboardv2



# set bucket names 
queueBucketName = "inputs"
outputBucketName = "outputs"


# minio connection
minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,access_key = minioUser, secret_key=minioPasswd, secure=False)

# RabbitMQ connection
hostname= os.environ['RABBIT_HOST'] if 'RABBIT_HOST' in os.environ else 'localhost'

# connecting RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=hostname))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='DataQueue')

print( ' [*] Waiting for messages. To exit press CTRL+C' )
print("DataQueue")


# callback after receiving the data from the data collector 
def callback(ch, method, properties, body):
    print( " [x] Received the data from Data collector")

    # converting the data from json to list format 
    json_to_list = json.loads(body)
    # convert that into the dataframe
    df = pd.DataFrame(json_to_list)
    # Sending to Minio
    createBuckets()
    # convert the dataframe to the csv
    csv = df.to_csv().encode('utf-8')
    # store it in the minio bucket
    minioClient.put_object(queueBucketName,"/games/games.csv",data=BytesIO(csv),length=len(csv),content_type='application/csv')


def createBuckets():
    if  not minioClient.bucket_exists(queueBucketName):
        minioClient.make_bucket(queueBucketName)
    if not minioClient.bucket_exists(outputBucketName):
        minioClient.make_bucket(outputBucketName)
   

# data consuming and calling the callback
channel.basic_consume(queue='DataQueue', auto_ack=False, on_message_callback=callback)

channel.start_consuming()


