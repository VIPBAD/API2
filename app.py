import os
from flask import Flask, request, render_template, url_for, redirect, session
# register search blueprint (search.py)
from search import bp as search_bp

app = Flask(__name__)
# set a simple secret key for session handling (override with env SECRET_KEY in production)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# register blueprint that provides /search and /pick_cookie
app.register_blueprint(search_bp)


@app.route("/")
def home():
    # keep reading params if the MINI app passes them, but home is mostly static
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    # Home page: show Join button which links to /join preserving params
    return render_template("home.html", audio_url=audio_url, title=title, thumb=thumb)


@app.route("/join")
def join():
    """
    New join confirmation/options page.
    Clicking Join Music on home will land here. From here the user can confirm
    and then be taken to /player (we preserve query params).
    """
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")
    # Optional user info (MINI app may supply them)
    username = request.args.get("username", "")
    user_id = request.args.get("user_id", "")
    avatar = request.args.get("avatar", "")
    return render_template("join.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist,
                           username=username, user_id=user_id, avatar=avatar)


@app.route("/player")
def player():
    """
    Plays the provided audio. If username/user_id/avatar are present we store them
    in the session so /profile can show the joining user's information.
    Also accepts an optional cookie param (from search's /pick_cookie) so external
    playback helpers can use that cookie.
    """
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Unknown Title")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")

    # store any provided user info in session for profile page
    username = request.args.get("username")
    user_id = request.args.get("user_id")
    avatar = request.args.get("avatar")
    if username:
        session['username'] = username
    if user_id:
        session['user_id'] = user_id
    if avatar:
        session['avatar'] = avatar

    # optional cookie param (search page picks it and passes on)
    cookie = request.args.get("cookie", "")

    # If an 'auto_play' query param is given, the JS in player will try to auto-play.
    auto_play = request.args.get("auto_play", "")

    return render_template("player.html", audio_url=audio_url, title=title, thumb=thumb,
                           artist=artist, cookie=cookie, auto_play=auto_play)


@app.route("/profile")
def profile():
    """
    Profile page prefers explicit query params but falls back to session values saved
    when a user joined the player.
    """
    username = request.args.get("username") or session.get("username", "VIPBAD")
    user_id = request.args.get("user_id") or session.get("user_id", "8016771632")
    avatar = request.args.get("avatar") or session.get("avatar") or url_for('static', filename='img/avatar.png')

    # Provide favorites/recently_played placeholders (you likely have your own backend storage)
    favorites = []  # load from your storage / API
    recently_played = []  # load from your storage / API

    return render_template("profile.html", username=username, user_id=user_id, avatar=avatar,
                           favorites=favorites, recently_played=recently_played)


@app.route("/settings")
def settings():
    # keep existing settings view as before (render template)
    # You can extend the settings route to persist settings server-side if needed.
    # For now keep client-side localStorage based controls as before.
    return render_template("settings.html")


if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
