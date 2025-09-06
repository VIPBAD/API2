import os
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def home():
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    avatar = request.args.get("avatar", url_for('static', filename='img/avatar.png'))
    return render_template("home.html", audio_url=audio_url, title=title, thumb=thumb, avatar=avatar)

@app.route("/player")
def player():
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Unknown Title")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")
    return render_template("player.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    results = [
        {"title": "Rondi Tere Layi", "artist": "Speed Records", "thumb": url_for('static', filename='img/sample1.jpg'), "audio": ""},
        {"title": "Sample Track", "artist": "Artist", "thumb": url_for('static', filename='img/sample2.jpg'), "audio": ""},
    ]
    return render_template("search.html", q=q, results=results)

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
