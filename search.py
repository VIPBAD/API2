import os
import glob
import random
from flask import Blueprint, render_template, request, url_for

search_bp = Blueprint("search", __name__, template_folder="templates")


def cookie_txt_file():
    """
    Pick a random .txt cookie file from cookies/ folder and log chosen file into cookies/logs.csv
    """
    folder_path = os.path.join(os.getcwd(), "cookies")
    os.makedirs(folder_path, exist_ok=True)
    filename = os.path.join(folder_path, "logs.csv")
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        # no cookie files, raise or return None depending on your need
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt = random.choice(txt_files)
    with open(filename, "a") as file:
        file.write(f"Chosen File: {cookie_txt}\n")
    return cookie_txt


@search_bp.route("/search")
def search():
    q = request.args.get("q", "")
    # Try to choose cookie file (optional, will not break on failure)
    cookie_info = None
    try:
        cookie_info = cookie_txt_file()
    except Exception:
        cookie_info = None

    # Example results with sample mp3s so clicking plays a song:
    results = [
        {
            "title": "Rondi Tere Layi",
            "artist": "Speed Records",
            "thumb": url_for("static", filename="img/sample1.jpg"),
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        },
        {
            "title": "Sample Track",
            "artist": "Artist",
            "thumb": url_for("static", filename="img/sample2.jpg"),
            "audio": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        },
    ]

    # If you want, you can use the query 'q' to filter results here.
    if q:
        results = [r for r in results if q.lower() in r["title"].lower() or q.lower() in r["artist"].lower()]

    return render_template("search.html", q=q, results=results, cookie_info=cookie_info)
