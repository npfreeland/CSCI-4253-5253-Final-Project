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


# get the list of players currently in the NBA from the Minio server
def getActivePlayers():
    # Create a new bucket on the Minio server
    # Retrieve the list of current NBA players
    players = Player.get_active_players()

    # Save the list of players as a JSON file on the Minio server
    json_data = json.dumps(players)
    minioClient.put_object('nba-statistics-bucket', 'players.json', json_data, 'application/json')

    # Retrieve the list of players from the Minio server
    try:
        data = minioClient.get_object('nba-statistics-bucket', 'players.json')
        json_data = data.read()
        players = json.loads(json_data)
    except ResponseError as err:
        print(err)

# same can be done for other things like teams, standings, etc.

# Retrieve the current year
current_year = datetime.now().year

# # Retrieve the game data for the last 10 years
# for year in range(current_year - 10, current_year):
#     # Retrieve the game data for the current year
#     games = ScoreboardV2.ScoreboardV2(league_id='00', season=year).get_data_frames()

#     # Save the game data as a .csv file on the Minio server
#     csv_data = games.to_csv()
#     client.put_object('nba-data', f'games_{year}.csv', csv_data, 'text/csv')

# # Retrieve the game data for the current year from the Minio server
# try:
#     data = client.get_object('nba-data', f'games_{current_year}.csv')
#     csv_data = data.read()
#     games = pd.read_csv(StringIO(csv_data))
# except ResponseError as err:
#     print(err)

# # Fetch player statistics and store them in the Minio bucket
# player_stats = nba.player_stats()
# minio_client.put_object('nba-statistics-bucket', 'player-statistics.json', player_stats)

# # Fetch game schedules and store them in the Minio bucket
# schedules = nba.schedule()
# minio_client.put_object('nba-statistics-bucket', 'schedules.json', schedules)

# # Fetch historical data and store it in the Minio bucket
# historical_data = nba.historical()
# minio_client.put_object('nba-statistics-bucket', 'historical-data.json', historical_data)