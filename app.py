import os
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__)

@app.route("/")
def home():
    # Only show the join button; redirect to player on click with preserved params
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    return render_template("home.html", audio_url=audio_url, title=title, thumb=thumb)

@app.route("/player")
def player():
    # This route plays the audio only after joining
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Unknown Title")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")
    return render_template("player.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist)

@app.route("/profile")
def profile():
    # Use the joining user's first name, user ID, and profile picture
    username = request.args.get("username", "")
    user_id = request.args.get("user_id", "")
    avatar = request.args.get("avatar", url_for('static', filename='img/avatar.png'))
    return render_template("profile.html", username=username, user_id=user_id, avatar=avatar)

@app.route("/settings")
def settings():
    # Improved settings with favorites and recently played
    favorites = [
        {"title": "Rondi Tere Layi", "artist": "Speed Records", "thumb": url_for('static', filename='img/sample1.jpg')},
        {"title": "Sample Track", "artist": "Artist", "thumb": url_for('static', filename='img/sample2.jpg')}
    ]
    recently_played = [
        {"title": "Recent Song 1", "artist": "Recent Artist 1", "thumb": url_for('static', filename='img/sample3.jpg')},
        {"title": "Recent Song 2", "artist": "Recent Artist 2", "thumb": url_for('static', filename='img/sample4.jpg')}
    ]
    return render_template("settings.html", favorites=favorites, recently_played=recently_played)

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
