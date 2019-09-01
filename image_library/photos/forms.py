from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField

from wtforms import SubmitField
from wtforms.validators import ValidationError, Length, DataRequired


class PhotoForm(FlaskForm):
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save phoyo')
