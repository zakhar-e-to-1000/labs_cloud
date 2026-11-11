import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "done": self.done}


with app.app_context():
    db.create_all()  # створює таблиці, якщо їх ще немає


@app.get("/tasks")
def list_tasks():
    return jsonify([t.to_dict() for t in Task.query.all()])


@app.post("/tasks")
def create_task():
    data = request.get_json()
    task = Task(title=data["title"])
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201