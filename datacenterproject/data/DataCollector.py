import pika
import numpy as np
import json
import pandas as pd
import matplotlib.pylab as plt
import random as r
# pip install nba_api
import nba_api as nba
import nba_api.stats.endpoints as ep
import os


# RabbitMQ connection
hostname= os.environ['RABBIT_HOST'] if 'RABBIT_HOST' in os.environ else 'localhost'
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=hostname))
channel = connection.channel()



# Declare a queue for teams 
channel.queue_declare(queue='DataQueue')

from nba_api.stats.endpoints import leaguegamefinder


# Query for games where the Celtics were playing
gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
# The first DataFrame of those returned is what we want.
games = gamefinder.get_data_frames()[0]
games = games.dropna(how='any',axis=0)


# Convert the dataframe into the list 
list_to_pass = [games.columns.values.tolist()] + games.values.tolist()

# dump the list into the json format to send to the message queue
json_string = json.dumps(list_to_pass)




channel.basic_publish(exchange='',
                      routing_key='DataQueue',
                      body=json_string)
print( " [x] Sent the data to the Data Analyzer!!" )
connection.close()