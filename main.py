from  flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
Bootstrap5(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy()
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    todo_list = Todo.query.all()
    total_todo = Todo.query.count()
    completed_todo = Todo.query.filter_by(status=True).count()
    uncompleted_todo = total_todo - completed_todo
    return render_template("index.html", **locals())


@app.route("/add", methods=["GET","POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, status=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/update/<int:todo_id>", methods=["GET","POST"])
def update(todo_id):
    update_todo = Todo.query.filter_by(id=todo_id).first()
    update_todo.status = not update_todo.status
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    delete_todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(delete_todo)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

