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