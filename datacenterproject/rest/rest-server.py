from flask import Flask,  render_template  
from minio import Minio
import os
import csv
app = Flask(__name__)

def get_data():
    minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
    minioUser = os.getenv("MINIO_USER") or "rootuser"
    minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
    minioClient = Minio(minioHost,access_key = minioUser, secret_key=minioPasswd, secure=False)
    queueBucketName = "inputs"
    outputBucketName = "outputs"

    # scores
    minioClient.fget_object(outputBucketName,"csv/scores.csv","./static/csv/scores.csv")
    # Players
    minioClient.fget_object(outputBucketName,"csv/top_10_players_stats.csv","./static/csv/top_10_players_stats.csv")
    # shortchart
    minioClient.fget_object(outputBucketName,"img/Giannis Antetokounmpo.png","./static/images/Giannis Antetokounmpo.png")
    minioClient.fget_object(outputBucketName,"img/Joel Embiid.png","./static/images/Joel Embiid.png")
    minioClient.fget_object(outputBucketName,"img/Kevin Durant.png","./static/images/Kevin Durant.png")
    minioClient.fget_object(outputBucketName,"img/Nikola Jokic.png","./static/images/Nikola Jokic.png")
    minioClient.fget_object(outputBucketName,"img/Stephen Curry.png","./static/images/Stephen Curry.png")


@app.route('/')
def home():
    get_data()
    #scores
    with open("./static/csv/scores.csv") as file:
        score_reader = csv.reader(file)
        with open("./static/csv/top_10_players_stats.csv") as stats_file:
            player_reader = csv.reader(stats_file)
            return render_template('home.html',html_score_reader=score_reader,html_player_reader=player_reader)


if __name__=='__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)