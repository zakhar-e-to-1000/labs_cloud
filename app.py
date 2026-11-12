import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.Integer, default=0)
    description = db.Column(db.String(600), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "reviews": self.reviews,
            "description": self.description
        }


with app.app_context():
    db.create_all()  # створює таблиці, якщо їх ще немає


@app.get("/films")
def list_films():
    return jsonify([f.to_dict() for f in Film.query.all()])


@app.post("/films")
def create_film():
    data = request.get_json(silent=True)
    data.setdefault("reviews", None)
    data.setdefault("description", None)
    film = Film(title=data["title"], duration=data["duration"], reviews=data["reviews"], description=data["description"])
    db.session.add(film)
    db.session.commit()
    return jsonify(film.to_dict()), 201
