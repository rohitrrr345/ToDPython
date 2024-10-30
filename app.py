from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TODO.db'
db = SQLAlchemy(app)

# Define the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} {self.title} {self.desc}"

# Route for the homepage
@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()  

    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

# Route for the products page
@app.route("/products")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return "<p>These are products</p>"

# Route for deleting a todo item
@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:  # Check if the todo item exists
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('hello_world'))

# Run the app and initialize the database tables
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the tables if they don't exist
    app.run(debug=True, port=8000)
