import os
from typing import Optional
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

class Base(DeclarativeBase):
  pass
db = SQLAlchemy(app, model_class=Base)


class Film(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    duration: Mapped[int] = mapped_column(db.Integer, nullable=False)
    reviews: Mapped[int] = mapped_column(db.Integer, default=0)
    description: Mapped[Optional[str]] = mapped_column(db.String(600), nullable=True)

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
    films = db.session.execute(db.select(Film)).scalars()
    return jsonify([f.to_dict() for f in films])


@app.post("/films")
def create_film():
    data = request.get_json(silent=True)
    data.setdefault("reviews", None)
    data.setdefault("description", None)
    film = Film(title=data["title"], duration=data["duration"], reviews=data["reviews"], description=data["description"])
    db.session.add(film)
    db.session.commit()
    return jsonify(film.to_dict()), 201
