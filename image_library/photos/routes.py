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

photos = Blueprint('photos', __name__)


@photos.route("/photo/new", methods=['GET', 'POST'])
@login_required
def add_photo():
    form = PhotoForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        photo = Photo(
            image_file=picture_file,
            author=current_user
        )
        db.session.add(photo)
        db.session.commit()
        flash('Your image has been added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_photo.html',
                           form=form,
                           legend='Add Photo')


@photos.route("/photo/<int:photo_id>")
def photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo.html',
                           photo=photo)
