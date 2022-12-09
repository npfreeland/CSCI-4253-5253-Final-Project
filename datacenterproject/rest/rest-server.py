from flask import Flask,  render_template  
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import LeagueStandings
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


if __name__=='__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)