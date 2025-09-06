import os
from flask import Flask, request, render_template, url_for
from search import search_bp  # import search blueprint

app = Flask(__name__)

# Register search blueprint
app.register_blueprint(search_bp, url_prefix="/search")

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
def search_page():
    q = request.args.get("q", "")
    return render_template("search.html", q=q, results=[])

@app.route("/profile")
def profile():
    username = request.args.get("username", "VIP")
    return render_template("profile.html", username=username)

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/favorites")
def favorites():
    return render_template("favorites.html")

@app.route("/recently-played")
def recently_played():
    return render_template("recently_played.html")

@app.route("/connected-users")
def connected_users():
    return render_template("connected_users.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
