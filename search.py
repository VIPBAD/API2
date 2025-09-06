import os
import glob
import random
import logging
import yt_dlp
from flask import Blueprint, request, jsonify

search_bp = Blueprint("search", __name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pick random cookie file
def cookie_txt_file():
    folder_path = os.path.join(os.getcwd(), "cookies")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in cookies/ folder")
    return random.choice(txt_files)

# API route for searching songs
@search_bp.route("/api", methods=["GET"])
def search_api():
    q = request.args.get("q", "")
    if not q:
        return jsonify({"error": "Query param 'q' is required"}), 422

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "geo_bypass": True,
        "noplaylist": False,
        "ignoreerrors": True,
        "format": "bestaudio/best",
        "cookiefile": cookie_txt_file(),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{q}", download=False)
            if not info or "entries" not in info:
                return jsonify([])

            results = []
            for entry in info["entries"]:
                if not entry:
                    continue
                results.append({
                    "title": entry.get("title", "Unknown"),
                    "artist": entry.get("uploader", "YouTube"),
                    "thumb": entry.get("thumbnail", ""),
                    "audio": entry.get("url", ""),  # direct stream url
                })
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return jsonify({"error": str(e)}), 500
