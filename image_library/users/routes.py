from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    url_for, request
)
from flask_login import (
    current_user,
    logout_user,
    login_user,
    login_required
)
from image_library.models import User, Photo
from image_library.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm
)
from image_library import db, bcrypt
from image_library.users.utils import save_picture
from image_library.config import Config

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            admin=form.admin.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(
                form.picture.data,
                True,
                Config.SAVE_IMAGE_LOCAL
            )
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.admin = form.admin.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.admin.data = current_user.admin

    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)

    return render_template(
        'account.html',
        title='Account',
        image_file=image_file,
        form=form
    )


@users.route("/user/<string:username>")
def user_photos(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    photos = Photo.query.filter_by(author=user)\
        .order_by(Photo.date_posted.desc())\
        .paginate(page=page, per_page=int(Config.PHOTOS_PER_PAGE))
    return render_template('user_photos.html', photos=photos, user=user)
