from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

import os

basedir = os.path.abspath(os.path.dirname(__file__))
database_file = "sqlite:///{}".format(os.path.join(basedir, "app.db"))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.secret_key = 'super secret key'
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(120))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<Author {}>'.format(self.last_name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(140))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref='books')

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id

    def __repr__(self):
        return '<Book {}>'.format(self.title)


@app.route('/')
def about():
    return render_template("home.html")


@app.route("/authors", methods=["GET", "POST"])
def author_create():
    if request.form:
        last_name = request.form.get("last_name")
        first_name = request.form.get("first_name")

        new_author = Author(first_name=first_name, last_name=last_name)

        db.session.add(new_author)
        db.session.commit()
        flash('Your ticket has been added to the queue')
    authors = Author.query.all()
    return render_template("index.html", authors=authors)


@app.route("/authors/update", methods=["POST"])
def author_update():
    newlast_name = request.form.get("newlast_name")
    newfirst_name = request.form.get("newfirst_name")
    oldfirst_name = request.form.get("oldfirst_name")
    oldlast_name = request.form.get("oldlast_name")
    author = Author.query.filter_by(last_name=oldlast_name, first_name=oldfirst_name).first()
    author.last_name = newlast_name
    author.first_name = newfirst_name
    db.session.commit()
    return redirect("/authors")


@app.route("/authors/delete", methods=["POST"])
def author_delete():
    last_name = request.form.get("last_name")
    first_name = request.form.get("first_name")
    author = Author.query.filter_by(last_name=last_name, first_name=first_name).first()
    db.session.delete(author)
    db.session.commit()
    return redirect("/authors")


@app.route("/books", methods=["GET", "POST"])
def book_create():
    if request.form:
        title = request.form.get("title")
        description = request.form.get("description")
        author_id = request.form.get("author_id")
        new_book = Book(title=title, description=description, author_id=author_id)

        db.session.add(new_book)
        db.session.commit()
    books = Book.query.all()
    return render_template("book.html", books=books)


@app.route("/books/delete", methods=["POST"])
def book_delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/books")

if __name__ == "__main__":
    app.run(port=8888, debug=True)

