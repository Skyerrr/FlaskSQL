from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfCA6O6donuWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(250), unique=False, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


class BookForm(FlaskForm):
    book = StringField('Book name', validators=[DataRequired()])
    author = StringField('Author name', validators=[DataRequired()])
    rating = SelectField("Book Rating", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')


class BookEdit(FlaskForm):
    rating = SelectField("Book Rating", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                         validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteBook(FlaskForm):
    submit = SubmitField('CLICK HERE TO DELETE NOW')


db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", all_books=all_books, len=len(all_books))


@app.route('/add', methods=["GET", "POST"])
def add():
    form = BookForm()
    if request.method == "POST":
        new_book = Book(book=request.form["book"], author=request.form["author"], rating=request.form["rating"])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html', form=form)


@app.route('/edit', methods=["GET", "POST"])
def edit():
    form = BookEdit()
    if request.method == "POST":
        book_id = request.args.get('id')
        rating_book = request.form["rating"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = rating_book
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html", form=form, book=book_selected)


@app.route('/delete', methods=["GET", "POST"])
def delete():
    form = DeleteBook()
    if request.method == "POST":
        book_id = request.args.get('id')
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("delete.html", form=form, book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
