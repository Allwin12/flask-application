import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)

from models import Book, User

admin = Admin(app, name='Allwin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/user")
def add_user():
    name = request.args.get('name')
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return "User added. user name={}".format(user.name)
    except Exception as e:
        return str(e)


@app.route("/get-names")
def get_all_names():
    try:
        user = User.query.all()
        return jsonify([e.serialize() for e in user])
    except Exception as e:
        return str(e)


@app.route("/add")
def add_book():
    name = request.args.get('name')
    author = request.args.get('author')
    published = request.args.get('published')
    try:
        book = Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
        return str(e)


@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
