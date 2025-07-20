import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict

load_dotenv()
app = Flask(__name__)

print("Environment variables loaded:")
print(f"MYSQL_DATABASE: {os.getenv('MYSQL_DATABASE')}")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_PASSWORD: {os.getenv('MYSQL_PASSWORD')}")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"URL: {os.getenv('URL')}")

if os.getenv("TESTING") == "true":
    mydb = SqliteDatabase("file:memory?mode=memory&cache=shared", uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306,
    )


class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb


mydb.connect()
mydb.create_tables([TimelinePost])

# define nav items
nav_items = [
    {"name": "Home", "url": "/"},
    {"name": "About", "url": "/about"},
    {"name": "Work", "url": "/work"},
    {"name": "Hobbies", "url": "/hobbies"},
    {"name": "Education", "url": "/education"},
    {"name": "Travel", "url": "/travel"},
    {"name": "Timeline", "url": "/timeline"},
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


@app.route("/education")
def education():
    education = [
        {
            "school": "Carleton University",
            "date": "2022 - 2027",
        },
        {
            "school": "Oakville Trafalgar High School",
            "date": "2018 - 2022",
        },
    ]
    return render_template("education.html", education=education)


@app.route("/travel")
def travel():
    locations = [
        {"name": "Paris, France", "lat": 48.8566, "lng": 2.3522},
        {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
        {"name": "Vancouver, Canada", "lat": 49.2827, "lng": -123.1207},
        {"name": "Ottawa, Canada", "lat": 45.4215, "lng": -75.6972},
        {"name": "Toronto, Canada", "lat": 43.6532, "lng": -79.3832},
        {"name": "New Delhi, India", "lat": 28.6139, "lng": 77.2090},
        {"name": "Manchester, UK", "lat": 53.4808, "lng": -2.2426},
        {"name": "Newcastle, UK", "lat": 54.9783, "lng": -1.6178},
        {"name": "Glasgow, Scotland", "lat": 55.8642, "lng": -4.2518},
        {"name": "Rome, Italy", "lat": 41.9028, "lng": 12.4964},
        {"name": "San Francisco, USA", "lat": 37.7749, "lng": -122.4194},
        {"name": "Seattle, Washington, USA", "lat": 47.6062, "lng": -122.3321},
        {"name": "Hawaii, USA", "lat": 19.8968, "lng": -155.5828},
    ]
    return render_template("travel.html", locations=locations)


@app.route("/api/timeline_post", methods=["POST"])
def post_time_line_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    content = request.form.get("content", "").strip()

    # Validation
    if not name:
        return "Invalid name", 400
    if not content:
        return "Invalid content", 400
    if not email or ("@" not in email or "." not in email):
        return "Invalid email", 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route("/api/timeline_post", methods=["GET"])
def get_time_line_post():
    return {
        "timeline_posts": [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route("/timeline")
def timeline():
    return render_template("timeline.html", title="Timeline")
