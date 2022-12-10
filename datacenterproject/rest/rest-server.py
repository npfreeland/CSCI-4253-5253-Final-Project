from flask import Flask,  render_template  
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import LeagueStandings

from nba_api.stats.endpoints._base import Endpoint
from nba_api.stats.library.http import NBAStatsHTTP
from nba_api.stats.library.parameters import PerMode36, LeagueIDNullable
app = Flask(__name__)




@app.route('/')
def home():
    List_Of_Players = ["203999"]
    List_Of_PlayersCareerStats = []
    for i in List_Of_Players:
        i = PlayerCareerStats(player_id=i).season_totals_regular_season.get_data_frame()
        i = i[i["SEASON_ID"]=="2022-23"]
        print(i)
        List_Of_PlayersCareerStats.append(i.to_dict(orient = 'list'))
        print(List_Of_PlayersCareerStats)
    return render_template('home.html', HTML_List_Of_PlayersCareerStats = List_Of_PlayersCareerStats)


if __name__=='__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)