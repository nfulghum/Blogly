from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'sdfsdfs'

connect_db(app)
db.create_all()


@app.route('/')
def root():
    return redirect('/users')


@app.route('/users', methods=["GET", "POST"])
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/new', methods=["GET", "POST"])
def create_new_users():
    return render_template('new.html')


@app.route('/', methods=["GET", "POST"])
def create_new_users_form():
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"] or None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/<int:user_id>')
def show_users(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('show.html', user=user)


@app.route('/<int:user_id>/edit')
def edit_users(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)


@app.route('/<int:user_id>/edit', methods=["POST"])
def update_edit_users(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
