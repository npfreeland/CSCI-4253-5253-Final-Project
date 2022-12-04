import pika

import os
hostname= os.environ['RABBIT_HOST'] if 'RABBIT_HOST' in os.environ else 'localhost'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=hostname))
channel = connection.channel()

channel.queue_declare(queue='DataQueue')

import numpy as np
import json
import pandas as pd
import matplotlib.pylab as plt
import random as r
# %matplotlib inline

# pip install nba_api
import nba_api as nba
import nba_api.stats.endpoints as ep


from nba_api.stats.static import teams

nba_teams = teams.get_teams()
# Select the dictionary for the Celtics, which contains their team ID
celtics = [team for team in nba_teams if team['abbreviation'] == 'BOS'][0]
celtics_id = celtics['id']

from nba_api.stats.endpoints import leaguegamefinder

# Query for games where the Celtics were playing
gamefinder = leaguegamefinder.LeagueGameFinder(league_id_nullable='00')
# The first DataFrame of those returned is what we want.
games = gamefinder.get_data_frames()[0]
games = games.dropna(how='any',axis=0)
games = games[games.SEASON_ID.str[-4:] != '2022']
games = games[games.SEASON_ID.str[-4:] != '2021']
games.head(10)

# print("games")
print(type(games))
# print(games.values.tolist())

print(games.columns.values.tolist())
list_to_pass = [games.columns.values.tolist()] + games.values.tolist()
json_string = json.dumps(list_to_pass)
print(type(json_string))
# print(json_string)
print(list_to_pass[0:2])



channel.basic_publish(exchange='',
                      routing_key='DataQueue',
                      body=json_string)
print( " [x] Sent 'Hello World!'" )
connection.close()