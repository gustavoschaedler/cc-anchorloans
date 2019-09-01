from image_library.models import Photo
from image_library.config import Config
from flask import Blueprint, render_template, request


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    photos = Photo.query.filter(Photo.approved == 1).order_by(
        Photo.date_posted.desc()).paginate(page=page, per_page=int(Config.PHOTOS_PER_PAGE))
    return render_template('home.html', photos=photos)
