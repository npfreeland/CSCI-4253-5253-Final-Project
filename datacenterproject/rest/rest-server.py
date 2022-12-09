from flask import Flask,  render_template  
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import leaguestandings
app = Flask(__name__)

@app.route('/')
def home():

    return render_template('home.html')

@app.route('/players')
def players():
    players = Player.get_active_players()
    return render_template('players.html', players=players)

@app.route('/standings')
def standings():
    standings = LeagueStandings.get_league_standings()
    eastern_standings = [team for team in standings if team.conference == 'East']
    western_standings = [team for team in standings if team.conference == 'West']
    return render_template('standings.html', eastern_standings=eastern_standings, western_standings=western_standings)

# # Define a route for handling search requests
# @app.route('/search', methods=['GET'])
# def search():
#     # Get the search query from the request parameters
#     query = request.args.get('q')

#     # Query the data in the Minio bucket to find the relevant results
#     player_stats = minio_client.get_object('nba-statistics-bucket', 'player-statistics.json')
#     data = player_stats.read().decode('utf-8')
#     results = [d for d in data if query in d['name']]

#     # Pass the results to the template for display
#     return render_template('search-results.html', results=results)

# Define a route for displaying comparison options
# @app.route('/compare')
# def compare():
#     # Fetch the available players and teams from the Minio bucket
#     player_stats = minio_client.get_object('nba-statistics-bucket', 'player-statistics.json')
#     players = player_stats.read().decode('utf-8')
#     team_stats = minio_client.get_object('nba-statistics-bucket', 'team-statistics.json')
#     teams = team_stats.read().decode('utf-8')
#     # Pass the available players and teams to the template
#     return render_template('compare.html', players=players, teams=teams)

# # Define a route for handling comparison requests
# @app.route('/compare', methods=['POST'])
# def compare_stats():
#     # Get the selected players and teams from the request parameters
#     players = request.form.getlist('players')
#     teams = request.form.getlist('teams')

#     # Fetch the statistics for the selected players and teams from the Minio bucket
#     player_stats = minio_client.get_object('nba-statistics-bucket', 'player-statistics.json')
#     player_data = player_stats.read().decode('utf-8')
#     selected_players = [d for d in player_data if d['name'] in players]
#     team_stats = minio_client.get_object('nba-statistics-bucket', 'team-statistics.json')
#     team_data = team_stats.read().decode('utf-8')
#     selected_teams = [d for d in team_data if d['teamName'] in teams]

#     # Pass the selected player and team data to the template for display
#     return render_template('compare-results.html', players=selected_players, teams=selected_teams)


#================================================================================================
# To modify the code to dynamically fetch the data from the Minio bucket using the Minio Python client, you could add a route to the Flask app that retrieves the data from the bucket and returns it as a JSON object. Here is an example of how you could do this:

# # Define a route for fetching player statistics from the Minio bucket
# @app.route('/player-stats')
# def player_stats():
#     # Fetch the player statistics from the Minio bucket
#     player_stats = minio_client.get_object('nba-statistics-bucket', 'player-statistics.json')
#     data = player_stats.read().decode('utf-8')
#     # Return the player statistics as a JSON object
#     return jsonify(data)

# In this example, the player_stats() function uses the Minio Python client to fetch the player statistics data from the Minio bucket and return it as a JSON object.

# example html to go along with this code:
# You could then modify the JavaScript code to dynamically fetch the data from this route using an AJAX request. Here is an example of how you could do this:

# // Load the D3.js library
# <script src="https://d3js.org/d3.v5.min.js"></script>

# // Create a bar chart using D3.js
# <script>
#     // Fetch the player statistics data from the Flask app using an AJAX request
#     d3.json("/player-stats", function(error, data) {
#         if (error) throw error;

#         var margin = {top: 20, right: 20, bottom: 30, left: 40},
#             width = 960 - margin.left - margin.right,
#             height = 500 - margin.top - margin.bottom;

#         var x = d3.scaleBand()
#             .rangeRound([0, width])
#             .padding(0.1);

#         var y = d3.scaleLinear()
#             .rangeRound([height, 0]);

#         var svg = d3.select("body").append("svg")
#             .attr("width", width + margin.left + margin.right)
#             .attr("height", height + margin.top + margin.bottom)
#             .append("g")
#             .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

#         data.forEach(function(d) {
#             d.points = +d.points;
#             d.rebounds = +d.rebounds;
#             d.assists = +d.assists;
#         });

#         x.domain(data.map(function(d) { return d.name; }));
#         y.domain([0, d3.max(data, function(d) { return d.points; })]);

#         svg.selectAll(".bar")
#         .data(data)
#         .enter().append("rect")
#         .attr("class", "bar")
#         .attr("x", function(d) { return x(d.name); })
#         .attr("y", function(d) { return y(d.points); })
#         .attr("width", x.bandwidth())
#         .attr("height", function(d) { return height - y(d.points); });

#     svg.append("g")
#         .attr("transform", "translate(0," + height + ")")
#         .call(d3.axisBottom(x));

#     svg.append("g")
#         .call(d3.axisLeft(y));
# </script>

# # Define a route for the community sentiment page
# @app.route('/community-sentiment')
# def community_sentiment():
#     # Fetch the upcoming games from the Minio bucket
#     upcoming_games = minio_client.get_object('nba-statistics-bucket', 'upcoming-games.json')
#     games = upcoming_games.read().decode('utf-8')

#     # Render the community sentiment template
#     return render_template('community-sentiment.html', games=games)

@app.route('/team.html')
def team():
    return render_template("team.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

if __name__=='__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)