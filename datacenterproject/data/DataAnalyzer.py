import pika
import json
import os
from minio import Minio
import os
from io import BytesIO
import pandas as pd

queueBucketName = "inputs"
outputBucketName = "outputs"

minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,access_key = minioUser, secret_key=minioPasswd, secure=False)
hostname= os.environ['RABBIT_HOST'] if 'RABBIT_HOST' in os.environ else 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=hostname))
channel = connection.channel()

channel.queue_declare(queue='DataQueue')
from minio import Minio
minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
minioUser = os.getenv("MINIO_USER") or "rootuser"
minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
minioClient = Minio(minioHost,access_key = minioUser, secret_key=minioPasswd, secure=False)
print( ' [*] Waiting for messages. To exit press CTRL+C' )
print("DataQueue")
def callback(ch, method, properties, body):
    # print( " [x] Received %r" % (body,) )
    json_to_list = json.loads(body)
    print(json_to_list[0])
    df = pd.DataFrame(json_to_list)
    # Sending to Minio
    createBuckets()
    csv = df.to_csv().encode('utf-8')
    minioClient.put_object(queueBucketName,"Data.csv",data=BytesIO(csv),length=len(csv),content_type='application/csv')


def createBuckets():
    if  not minioClient.bucket_exists(queueBucketName):
        minioClient.make_bucket(queueBucketName)
    if not minioClient.bucket_exists(outputBucketName):
        minioClient.make_bucket(outputBucketName)
   


channel.basic_consume(queue='DataQueue', auto_ack=False, on_message_callback=callback)

channel.start_consuming()