import os
import json
from flask import Flask, request, render_template, url_for, jsonify, send_from_directory
from search import search_bp

app = Flask(__name__)
app.register_blueprint(search_bp)  # blueprint defines /search route

DATA_DIR = os.path.join(os.getcwd(), "data")
FAV_FILE = os.path.join(DATA_DIR, "favorites.json")
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(FAV_FILE):
    with open(FAV_FILE, "w") as f:
        json.dump([], f)


@app.route("/")
def home():
    # Do NOT show player UI here. Home only displays Join button (player opens on /player).
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    # Keep audio param so MINI app can forward it into Join link, but do not play here.
    audio_url = request.args.get("audio", "")
    return render_template("home.html", title=title, thumb=thumb, audio_url=audio_url)


@app.route("/player")
def player():
    # Plays audio passed by query params.
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Unknown Title")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")
    return render_template("player.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist)


@app.route("/profile")
def profile():
    username = request.args.get("username", "VIPBAD")
    user_id = request.args.get("user_id", "8016771632")
    avatar = request.args.get("avatar", url_for('static', filename='img/avatar.png'))
    # Load favorites from server-side file:
    try:
        with open(FAV_FILE, "r") as f:
            favorites = json.load(f)
    except Exception:
        favorites = []
    return render_template("profile.html", username=username, user_id=user_id, avatar=avatar, favorites=favorites)


@app.route("/settings")
def settings():
    return render_template("settings.html")


# Simple API endpoints to manage favorites (used by client script)
@app.route("/api/favorites", methods=["GET", "POST", "DELETE"])
def api_favorites():
    if request.method == "GET":
        with open(FAV_FILE, "r") as f:
            data = json.load(f)
        return jsonify(data)

    if request.method == "POST":
        payload = request.json or {}
        item = payload.get("item")
        if not item:
            return jsonify({"error": "no item provided"}), 400
        with open(FAV_FILE, "r") as f:
            data = json.load(f)
        # avoid duplicates by audio url
        if not any(x.get("audio") == item.get("audio") for x in data):
            data.insert(0, item)  # newest first
            with open(FAV_FILE, "w") as f:
                json.dump(data, f, indent=2)
        return jsonify({"status": "ok", "favorites": data})

    if request.method == "DELETE":
        payload = request.json or {}
        audio_url = payload.get("audio")
        with open(FAV_FILE, "r") as f:
            data = json.load(f)
        data = [x for x in data if x.get("audio") != audio_url]
        with open(FAV_FILE, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "deleted", "favorites": data})


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
