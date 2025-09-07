import os
from flask import Flask, request, render_template, url_for, jsonify
import logging
from urllib.parse import parse_qs, unquote_plus
import json

app = Flask(__name__, static_folder="static", template_folder="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route("/")
def home():
    # basic landing page; mini app can open with query params for audio/title/thumb/avatar
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
    artist = request.args.get("artist", "Unknown")
    avatar = request.args.get("avatar", url_for('static', filename='img/avatar.png'))
    return render_template("player.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist, avatar=avatar)

@app.route("/profile")
def profile():
    """
    Telegram WebApp may send initData as query like:
    ?initData=user=%7B%22id%22%3A12345%2C%22first_name%22%3A%22Bob%22%7D&auth_date=...
    This function attempts to parse 'user' field (JSON) robustly without signature validation.
    """
    init_data = request.args.get("initData", "") or request.args.get("init_data", "")
    user_data = {
        "username": "VIP",
        "user_id": "",
        "photo_url": url_for('static', filename='img/avatar.png'),
        "first_name": ""
    }
    if init_data:
        try:
            # if full query-string passed, parse properly
            if "=" in init_data and "&" in init_data:
                parsed = parse_qs(init_data)
                # find 'user' key (could be 'user' or 'user=')
                user_json = parsed.get("user", ["{}"])[0]
                user_json = unquote_plus(user_json)
            else:
                # sometimes only user=... is provided directly
                if init_data.startswith("user="):
                    user_json = unquote_plus(init_data.split("user=", 1)[1])
                else:
                    # try to treat init_data as plain json
                    user_json = unquote_plus(init_data)
            user = json.loads(user_json) if user_json else {}
            user_data["username"] = user.get("username") or f"{user.get('first_name','User')}"
            user_data["first_name"] = user.get("first_name", "")
            user_data["user_id"] = user.get("id", "")
            # Telegram gives photo_url sometimes - else default
            user_data["photo_url"] = user.get("photo_url") or url_for('static', filename='img/avatar.png')
        except Exception as e:
            logger.warning("profile parsing failed: %s", e)
    return render_template("profile.html", **user_data)

# small API to demonstrate favorites placeholder (optional)
FAVORITES = []

@app.route("/api/favorites", methods=["GET", "POST", "DELETE"])
def api_favorites():
    if request.method == "GET":
        return jsonify(FAVORITES)
    if request.method == "POST":
        item = request.json.get("item")
        if item:
            FAVORITES.append(item)
        return jsonify({"ok": True, "count": len(FAVORITES)})
    if request.method == "DELETE":
        data = request.json or {}
        audio = data.get("audio")
        if audio:
            FAVORITES[:] = [f for f in FAVORITES if f.get("audio") != audio]
        return jsonify({"ok": True, "count": len(FAVORITES)})

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=PORT, debug=True)
