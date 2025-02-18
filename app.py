from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("template.html")

@app.route("/tags")
def tags():
    return render_template("tags.html")

@app.route("/labels")
def labels():
    return render_template("labels.html")

@app.route("/players")
def players():
    return render_template("players.html")

@app.route("/teams")
def teams():
    return render_template("teams.html")

if __name__ == "__main__":
    app.run(debug=True)