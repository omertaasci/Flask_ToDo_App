from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']

    with app.app_context():
        new_todo = Todo(content=content)
        db.session.add(new_todo)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
def complete_todo(id):
    with app.app_context():
        todo = Todo.query.get(id)
        todo.completed = not todo.completed
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete_todo(id):
    with app.app_context():
        todo = Todo.query.get(id)
        db.session.delete(todo)
        db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
