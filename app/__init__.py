from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# define nav items
nav_items = [
    {"name": "Home", "url": "/"},
    {"name": "About", "url": "/about"},
    {"name": "Work", "url": "/work"},
    {"name": "Hobbies", "url": "/hobbies"},
    {"name": "Education", "url": "/education"},
    {"name": "Travel", "url": "/travel"},
]


# make nav items global
@app.context_processor
def inject_nav_items():
    return dict(nav_items=nav_items)


# routes
@app.route("/")
def index():
    return render_template("index.html", title="Home")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/work")
def work():
    work_experiences = [
        {
            "company": "JSI Telecom",
            "role": "Software Developer",
            "date": "Sep 2025 - Dec 2025",
        },
        {"company": "MLH Fellowship", "role": "Fellow", "date": "Jun 2025 - Sep 2025"},
        {
            "company": "SunnySide",
            "role": "Software Engineer",
            "date": "Apr 2024 - Present",
        },
        {
            "company": "Global Affairs Canada",
            "role": "Junior Developer",
            "date": "Jun 2024 - Dec 2024",
        },
    ]
    return render_template("work.html", jobs=work_experiences)


@app.route("/hobbies")
def hobbies():
    hobbies = [
        {"name": "Chess", "image": "chess.png"},
        {"name": "Guitar", "image": "telecaster.webp"},
        {"name": "Bouldering", "image": "bouldering.jpg"},
    ]
    return render_template("hobbies.html", hobbies=hobbies)
