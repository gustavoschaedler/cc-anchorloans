from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash,
    abort
)
from flask_login import (
    login_required,
    current_user
)
from image_library import db
from image_library.models import Photo
from image_library.photos.forms import PhotoForm
from image_library.users.utils import save_picture
from image_library.config import Config

photos = Blueprint('photos', __name__)


@photos.route("/photo/new", methods=['GET', 'POST'])
@login_required
def add_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(
                form.picture.data,
                False,
                Config.SAVE_IMAGE_LOCAL
            )
            current_user.image_file = picture_file

        photo = Photo(
            image_file=picture_file,
            author=current_user,
            approved=current_user.admin
        )
        db.session.add(photo)
        db.session.commit()

        if current_user.admin == 1:
            flash('Your image has been added!', 'success')
        else:
            flash('Your image has been added!\nWaiting for approval.', 'warning')

        return redirect(url_for('main.home'))
    return render_template('create_photo.html',
                           form=form,
                           legend='Add Photo')


@photos.route("/photo/<int:photo_id>")
def photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo.html',
                           photo=photo)


@photos.route("/to_approval")
def to_approval():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.filter(Photo.approved == 0).order_by(
        Photo.date_posted.asc()).paginate(page=page, per_page=int(Config.PHOTOS_PER_PAGE))
    return render_template('to_approval.html', photos=photos)


@photos.route("/approve/<int:photo_id>/update", methods=['GET', 'POST'])
def approve(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user.admin != 1:
        abort(403)

    photo.approved = 1
    db.session.commit()
    flash('Photo has been approved!', 'success')

    return redirect(url_for('main.home'))
