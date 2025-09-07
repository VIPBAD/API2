import os
import json
import logging
from urllib.parse import parse_qs, unquote_plus
from flask import Flask, request, render_template, url_for, jsonify

app = Flask(__name__, static_folder="static", template_folder="templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("alexamusic")

# ---- Routes ----

@app.route("/")
def home():
    # Common params used by BotFather preview or direct links
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    # allow preview avatar for UI checks
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
    Parses initData-like query strings and falls back to provided avatar param.
    Use avatar param for quick BotFather preview testing.
    """
    init_data = request.args.get("initData") or request.args.get("init_data") or ""
    avatar_q = request.args.get("avatar") or request.args.get("photo_url") or ""
    user_data = {
        "username": "VIP",
        "user_id": "",
        "photo_url": url_for('static', filename='img/avatar.png'),
        "first_name": ""
    }

    # explicit avatar param takes priority (handy for BotFather preview)
    if avatar_q:
        user_data["photo_url"] = avatar_q

    if init_data:
        try:
            # If init_data looks like a query-string: user=%7B...%7D&auth_date=...
            if "=" in init_data and "&" in init_data:
                parsed = parse_qs(init_data)
                user_json = parsed.get("user", ["{}"])[0]
                user_json = unquote_plus(user_json)
            else:
                if init_data.startswith("user="):
                    user_json = unquote_plus(init_data.split("user=", 1)[1])
                else:
                    user_json = unquote_plus(init_data)
            if user_json:
                user = json.loads(user_json)
                user_data["username"] = user.get("username") or user.get("first_name") or user_data["username"]
                user_data["first_name"] = user.get("first_name", "")
                user_data["user_id"] = user.get("id", "")
                # possible photo fields
                photo_url = user.get("photo_url") or user.get("photo") or ""
                if photo_url:
                    user_data["photo_url"] = photo_url
        except Exception as e:
            logger.warning("profile parsing failed: %s", e)

    return render_template("profile.html", **user_data)

# small API for favorites (demo)
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

# debug helper to inspect what BotFather / telegram opens
@app.route("/debug-init")
def debug_init():
    return {"query": request.query_string.decode(), "args": request.args}

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=PORT, debug=True)
