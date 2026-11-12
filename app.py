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
    description: Mapped[Optional[str]] = mapped_column(
        db.String(600), nullable=True)

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
    stmt = db.select(Film)
    films = db.session.execute(stmt).scalars()
    return jsonify([f.to_dict() for f in films])


@app.post("/films")
def create_film():
    data = request.get_json(silent=True)
    data.setdefault("reviews", None)
    data.setdefault("description", None)
    film = Film(title=data["title"], duration=data["duration"],
                reviews=data["reviews"], description=data["description"])
    db.session.add(film)
    db.session.commit()
    return jsonify(film.to_dict()), 201


@app.get('/films/<int:film_id>')
def get_film(id):
    film = db.get_or_404(Film, id)
    return jsonify(film.to_dict()), 200


@app.delete('/films/<int:film_id>')
def delete_film(id):
    film = db.get_or_404(Film, id)
    db.session.delete(film)
    db.session.commit()
    return jsonify(film.to_dict()), 204


@app.put('/api/films/<int:film_id>')
def film_update(id):
    data = request.get_json(silent=True)
    film = db.get_or_404(Film, id)
    data.setdefault("reviews", film.reviews)
    data.setdefault("description", film.description)

    film.title = data["title"]
    film.duration = data["duration"]
    film.reviews = data["reviews"]
    film.description = data["description"]
    db.session.commit()
    db.session.add()
