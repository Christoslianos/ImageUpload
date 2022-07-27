from form import UploadForm
import os
import uuid
from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from method import upload_image_process

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'FJKHFKSDJGHDKSJHG'
app.config['UPLOADED_PHOTOS_DEST'] = 'static'


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        uploaded_image = form.photo.data
        filename = secure_filename(uploaded_image.filename)
        _, ext = os.path.splitext(filename)
        # creating a random name
        new_filename = uuid.uuid4().hex + ext
        image_with_palette, palette = upload_image_process(uploaded_image,
                                                           palette_division=10,
                                                           )
        image_with_palette_path = os.path.join(app.root_path, "static/uploads", new_filename)
        palette_path = os.path.join(app.root_path, "static/uploads", "pal" + new_filename)

        # save the image and palette
        image_with_palette.save(image_with_palette_path)
        palette.save(palette_path)

        return redirect(url_for("images", name=new_filename))
    return render_template('index.html', form=form, src="default")


@app.route('/images/<name>')
def images(name):
    process_img_relative_path = url_for("static", filename="/uploads/" + name)
    palette_relative_path = url_for("static", filename="/uploads/" + "pal" + name)

    return render_template("images.html", src=process_img_relative_path, src2=palette_relative_path)


if __name__ == '__main__':
    app.run(debug=True, port=7012)
