from flask import url_for, current_app
from PIL import Image
from image_library.external_service import service

import os
import secrets


def save_picture(form_picture, profile, save_local):
    if profile:
        path = 'static/profile'
    else:
        path = 'static/photos'

    if save_local == 'S3':
        picture_fn = service.upload_file_to_s3(form_picture, path)
    else:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext

        picture_path = os.path.join(
            current_app.root_path,
            path,
            picture_fn
        )
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn
