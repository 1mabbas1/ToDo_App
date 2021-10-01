from flask import Flask,render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = "sqlite://db.sqlite"
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean,)

@app.route("/")
def index():
    todolist = Todo.query.all()
    left = db.session.query(Todo).filter(Todo.complete == False).count()
    return render_template("index.html", todolist = todolist, left=left)

@app.route("/add", methods=["POST"])
def add():
    #add new list item
    title = request.form.get("title")
    new_item = Todo(title=title, complete=False)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete current item
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/edit/<int:todo_id>")
def update(todo_id):
    #update current item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/clearall")
def clearall():
    list = db.session.query(Todo).delete()
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()
    # hard coding a task for testing, can delete this code.
    # newtodo = Todo(title="todo1", complete=False)
    # db.session.add(newtodo)
    # db.session.commit()
    app.run(debug=True)

