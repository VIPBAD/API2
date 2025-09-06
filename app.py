import os
from flask import Flask, request, render_template, url_for, redirect
import yt_dlp
import logging
import glob
import random
import json

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pick a random .txt cookie file from cookies/ folder
def cookie_txt_file():
    folder_path = os.path.join(os.getcwd(), "cookies")
    filename = os.path.join(folder_path, "logs.csv")
    txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt = random.choice(txt_files)
    with open(filename, 'a') as file:
        file.write(f'Chosen File: {cookie_txt}\n')
    return cookie_txt

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
    results = []
    if q:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'geo_bypass': True,
            'noplaylist': False,
            'ignoreerrors': True,
            'format': 'bestaudio',
            'cachedir': False,
            'cookiefile': cookie_txt_file(),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch5:{q}", download=False)
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            title = entry.get('title', 'Unknown Title')
                            artist = entry.get('uploader', 'Unknown')
                            thumb = entry.get('thumbnail', '')
                            audio = ''
                            if 'requested_formats' in entry and entry['requested_formats']:
                                audio = entry['requested_formats'][0]['url']
                            elif 'url' in entry:
                                audio = entry['url']
                            results.append({
                                "title": title,
                                "artist": artist,
                                "thumb": thumb,
                                "audio": audio
                            })
        except Exception as e:
            logger.error(f"Search error for query {q}: {str(e)}")
            results = []

    return render_template("search.html", q=q, results=results)

@app.route("/profile")
def profile():
    # Get Telegram initData from query parameters
    init_data = request.args.get("initData", "")
    user_data = {}
    if init_data:
        try:
            # Parse initData (simplified, in real use validate with bot token)
            params = dict(param.split('=') for param in init_data.split('&'))
            user = json.loads(params.get('user', '{}'))
            user_data = {
                'username': user.get('username', 'Unknown User'),
                'user_id': user.get('id', ''),
                'photo_url': user.get('photo_url', url_for('static', filename='img/avatar.png'))
            }
        except Exception as e:
            logger.error(f"Error parsing initData: {str(e)}")
    return render_template("profile.html", username=user_data.get('username', 'VIP'), user_id=user_data.get('user_id', ''), photo_url=user_data.get('photo_url', ''))

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
    PORT = int(os.environ.get("PORT", 5050))
    app.run(host="0.0.0.0", port=PORT, debug=True)
