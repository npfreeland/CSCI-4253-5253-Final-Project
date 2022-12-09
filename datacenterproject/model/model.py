import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import os
import random as r
from minio import Minio
import joblib


# %matplotlib inline

# pip install nba_api
import nba_api as nba
import nba_api.stats.endpoints as ep
from nba_api.stats.static import teams
from nba_api.stats.static import players

from sklearn.model_selection import train_test_split

# Helper function to draw court
from matplotlib.patches import Circle, Rectangle, Arc




def draw_court(ax=None, color='black', lw=2, outer_lines=False):
        # If an axes object isn't provided to plot onto, just get current one
        if ax is None:
            ax = plt.gca()

        # Create the various parts of an NBA basketball court

        # Create the basketball hoop
        # Diameter of a hoop is 18" so it has a radius of 9", which is a value
        # 7.5 in our coordinate system
        hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

        # Create backboard
        backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

        # The paint
        # Create the outer box 0f the paint, width=16ft, height=19ft
        outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,
                            fill=False)
        # Create the inner box of the paint, widt=12ft, height=19ft
        inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,
                            fill=False)

        # Create free throw top arc
        top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                            linewidth=lw, color=color, fill=False)
        # Create free throw bottom arc
        bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                                linewidth=lw, color=color, linestyle='dashed')
        # Restricted Zone, it is an arc with 4ft radius from center of the hoop
        restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                        color=color)

        # Three point line
        # Create the side 3pt lines, they are 14ft long before they begin to arc
        corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,
                                color=color)
        corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
        # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
        # I just played around with the theta values until they lined up with the 
        # threes
        three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,
                        color=color)

        # Center Court
        center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color)
        center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                            linewidth=lw, color=color)

        # List of the court elements to be plotted onto the axes
        court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                        bottom_free_throw, restricted, corner_three_a,
                        corner_three_b, three_arc, center_outer_arc,
                        center_inner_arc]

        if outer_lines:
            # Draw the half court line, baseline and side out bound lines
            outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                    color=color, fill=False)
            court_elements.append(outer_lines)

        # Add the court elements onto the axes
        for element in court_elements:
            ax.add_patch(element)

        return ax

def create_shotchart(shot_data):
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,11))
    groups = shot_data.groupby('SHOT_ZONE_BASIC')
    for name, group in groups:
        ax.plot(group['LOC_X'], group['LOC_Y'], marker='.', linestyle='', label=name)
        # ax.set_title(player['full_name'] + ' Made Shots with the ' + team['full_name'])
    # ax.set(xlim=(, xmax), ylim=(ymin, ymax))

    plt.legend()
    # draw_court(outer_lines=True)
    # # Descending values along the axis from left to right
    # plt.xlim(300, -300)


    draw_court() 
    # Adjust plot limits to just fit in half court
    plt.xlim(-250, 250)
    # Descending values along th y axis from bottom to top
    # in order to place the hoop by the top of plot
    plt.ylim(422.5, -47.5)

    plt.savefig('sample.png')

    plt.show()


def get_game_data():
    #takes dataframe from minio bucket
    # songbyte = minioClient.fget_object(queueBucketName, "game_data.csv",f"./inputs/game_data.csv")
    games = pd.read_csv("./inputs/game_data.csv")
    games.columns = games.iloc[0]
    games = games.iloc[1:]
    games.drop(columns=games.columns[0], 
        axis=1, 
        inplace=True)
    
    return games


# def get_player_data():


# def get_team_data():



def create_models(X_train, y_train):

    # LinearSVC classification
    from sklearn.svm import LinearSVC
    lclf = LinearSVC(random_state=0, tol=1e-5, max_iter=1000)
    lclf.fit(X_train, y_train)

    print("LinearSVC model created")
    
    # KNN model attempt k=10
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn import preprocessing
    knn = KNeighborsClassifier(n_neighbors=10)
    knn.fit(X_train, y_train)
    print("KNN model created")

    # SVC prediction model attempt gamma set to 'scale' 
    from sklearn.svm import SVC
    from sklearn import svm
    clf = SVC(gamma='scale',probability=True)
    clf.fit(X_train, y_train)
    print("SVC model created")

    #BaggingSVC Ensemble classification
    from sklearn.svm import SVC
    from sklearn.ensemble import BaggingClassifier
    advclf = BaggingClassifier(base_estimator=SVC(gamma='scale'), n_estimators=10, random_state=0)
    advclf.fit(X_train, y_train)
    print("BaggingSVC model created")

    # Random Forest Classification model
    from sklearn.ensemble import RandomForestClassifier
    routcomes = RandomForestClassifier(max_depth=8, random_state=0, n_estimators=300)
    routcomes.fit(X_train, y_train)
    print("Random Forest model created")

    return lclf, knn, clf, advclf, routcomes


def test_models_single_team(lclf, knn, clf, advclf, routcomes, team_name='Denver Nuggets'):
    team_id = get_team_id(team_name)
    games = get_game_data()
    team_games = games[(games.TEAM_ID == team_id) & (games.SEASON_ID.str[-4:] == '2020')]

    team_outcomes = team_games[games.columns[7]]
    team_gamestats = team_games[games.columns[10:27]]
    # team_gamestats_mean = pd.DataFrame(team_gamestats.mean(axis=0)).transpose()
    # team_gamestats_mean_X = pd.DataFrame(np.repeat(team_gamestats_mean.values, len(team_games), axis=0))

    X_test = team_gamestats.to_numpy()
    # X_test = team_gamestats_mean_X.to_numpy()
    y_test = team_outcomes.to_numpy()

    scores_list = []
    scores_list.append(lclf.score(X_test,y_test))
    scores_list.append(knn.score(X_test, y_test))
    scores_list.append(clf.score(X_test,y_test))
    scores_list.append(advclf.score(X_test,y_test))
    scores_list.append(routcomes.score(X_test,y_test))

    return scores_list


def test_models_all(lclf, knn, clf, advclf, routcomes):
    team_names = []
    scores = []
    for team in nba_teams:
        tmp_scores = test_models_single_team(lclf, knn, clf, advclf, routcomes, team['full_name'])
        team_names.append(team['full_name'])
        scores.append(tmp_scores)
    scores_df = pd.DataFrame(scores,index=team_names,columns=['LinearSVC','KNN','SVC Predict','BaggingSVC','Random Forest'])

    return scores_df
    

def get_player_id(playername):
    player = [player for player in nba_players
            if player['full_name'] == playername][0]
    return str(player['id'])

def get_team_id(teamname):
    team = [team for team in nba_teams
            if team['full_name'] == teamname][0]
    return str(team['id'])


def get_player_shot_data(playername, teamname, season_nullable='2021-22'):
    player_id = get_player_id(playername)
    team_id = get_team_id(teamname)

    shot_data = ep.shotchartdetail.ShotChartDetail(player_id = players['id'], team_id = teams['id']).get_data_frames()[0]
    # shot data is shot positions data frame convert to csv
    return shot_data




if __name__=='__main__':
    minioHost = os.getenv("MINIO_HOST") or "localhost:9000"
    minioUser = os.getenv("MINIO_USER") or "rootuser"
    minioPasswd = os.getenv("MINIO_PASSWD") or "rootpass123"
    minioClient = Minio(minioHost,access_key = minioUser, secret_key=minioPasswd, secure=False)
    queueBucketName = "inputs"
    outputBucketName = "outputs"

    nba_teams = teams.get_teams()
    nba_players = players.get_players()

    # if models do not exist, create them
    path = '/home/User/Desktop/file.txt'
    if not os.path.exists('./trained_models/'):
        os.makedirs('./trained_models/')
        
        games = get_game_data()

        train_games = games[games.SEASON_ID.str[-4:] != '2020']

        outcomes = games[games.columns[7]]
        gamestats = games[games.columns[10:27]]    

        X_train = gamestats.to_numpy()
        y_train = outcomes.to_numpy()

        lclf, knn, clf, advclf, routcomes = create_models(X_train, y_train)


        # save models
        joblib.dump(lclf, "./trained_models/lclf.pkl")
        joblib.dump(knn, "./trained_models/knn.pkl")
        joblib.dump(clf, "./trained_models/clf.pkl")
        joblib.dump(advclf, "./trained_models/advclf.pkl")
        joblib.dump(routcomes, "./trained_models/routcomes.pkl")

    else:
        # load models
        lclf = joblib.load("./trained_models/lclf.pkl")
        knn = joblib.load("./trained_models/knn.pkl")
        clf = joblib.load("./trained_models/clf.pkl")
        advclf = joblib.load("./trained_models/advclf.pkl")
        routcomes = joblib.load("./trained_models/routcomes.pkl")


    scores_df = test_models_all(lclf, knn, clf, advclf, routcomes)
    # scores_df = scores_df.style.background_gradient(cmap ='YlOrRd').set_properties(**{'font-size': '20px'})
        # cmap ='viridis'
    
    scores_df.to_csv('scores.csv')