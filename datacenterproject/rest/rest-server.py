from flask import Flask,  render_template   
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/team.html')
def team():
    return render_template("team.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

if __name__=='__main__':
    # app.run()
    app.run(host="0.0.0.0", port=5000)
