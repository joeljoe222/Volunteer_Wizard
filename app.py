from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/eventManager")
def eventManager():
    return render_template("eventManager.html");

@app.route("/notificationSystem")
def notificationManager():
    return render_template("notificationSystem.html");

if __name__ == '__main__': app.run(host='0.0.0.0', debug=True)