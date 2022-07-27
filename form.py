from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired


class UploadForm(FlaskForm):
    photo = FileField("Upload Image",
                      validators=[
                          FileAllowed(["jpg", "jpeg", "png"]),
                          FileRequired('File field should not be empty')]
                      )