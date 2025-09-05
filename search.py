# New file: search.py
import os
import glob
import random
from flask import Blueprint, render_template, request, url_for, jsonify, current_app, session

bp = Blueprint("search", __name__, template_folder="templates", static_folder="static", url_prefix="")

# Pick a random .txt cookie file from cookies/ folder
def cookie_txt_file():
    folder_path = os.path.join(os.getcwd(), "cookies")
    filename = os.path.join(folder_path, "logs.csv")
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt = random.choice(txt_files)
    # ensure logs.csv exists
    os.makedirs(folder_path, exist_ok=True)
    with open(filename, 'a') as file:
        file.write(f'Chosen File: {cookie_txt}\n')
    return cookie_txt

@bp.route("/search")
def search():
    # sample placeholder results; extend search logic / API later
    q = request.args.get("q", "")
    results = [
        {
            "title": "Rondi Tere Layi",
            "artist": "Speed Records",
            "thumb": url_for('static', filename='img/sample1.jpg'),
            "audio": url_for('static', filename='audio/sample1.mp3')
        },
        {
            "title": "Sample Track",
            "artist": "Artist",
            "thumb": url_for('static', filename='img/sample2.jpg'),
            "audio": url_for('static', filename='audio/sample2.mp3')
        },
    ]
    # If an audio parameter is present, highlight that result and JS will auto-play
    auto_play = request.args.get("audio", "")
    return render_template("search.html", q=q, results=results, auto_play=auto_play)

@bp.route("/pick_cookie")
def pick_cookie():
    """
    Endpoint to pick a random cookie .txt and return its name/path.
    Client can call this to obtain a cookie file to be used for playback APIs.
    """
    try:
        cookie = cookie_txt_file()
        return jsonify({"ok": True, "cookie": cookie})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
