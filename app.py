import os
from flask import Flask, request, render_template, url_for
import yt_dlp
import logging
import glob
import random
import json
from database import Database

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

db = Database()

@app.route("/")
def home():
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Telegram Music")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    return render_template("home.html", audio_url=audio_url, title=title, thumb=thumb)

@app.route("/player")
def player():
    audio_url = request.args.get("audio", "")
    title = request.args.get("title", "Unknown Title")
    thumb = request.args.get("thumb", url_for('static', filename='img/default_album.png'))
    artist = request.args.get("artist", "YouTube")
    tg = request.environ.get('HTTP_X_TELEGRAM_INIT_DATA')
    if tg:
        user_data = json.loads(tg.split('user=')[1].split('&')[0])
        user_id = user_data.get('id')
        db.save_history(user_id, title, 0)  # Placeholder duration
    return render_template("play.html", audio_url=audio_url, title=title, thumb=thumb, artist=artist)

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
    tg = request.environ.get('HTTP_X_TELEGRAM_INIT_DATA')
    user_id = "0"
    recent = 0
    played = 0
    duration = 0
    if tg:
        user_data = json.loads(tg.split('user=')[1].split('&')[0])
        user_id = user_data.get('id')
        history = db.get_recent_history(user_id)
        recent = len(history)
        played = sum(1 for h in history)
        duration = sum(h.get('duration', 0) for h in history)
    return render_template("profile.html", username=user_data.get('username', 'No username'), user_id=user_id, recent=recent, played=played, duration=duration)

@app.route("/chating")
def chating():
    tg = request.environ.get('HTTP_X_TELEGRAM_INIT_DATA')
    chat_link = "https://t.me/TGINLINEMUSICBOT/Demo?startapp=-1002093247039"
    if tg:
        user_data = json.loads(tg.split('user=')[1].split('&')[0])
        user_id = user_data.get('id')
        # Real-time chat logic to be implemented with Telegram API
    return render_template("chating.html", chat_link=chat_link)

@app.route("/setting")
def setting():
    return render_template("setting.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
