from flask import Flask, request, redirect, send_file
from werkzeug.utils import secure_filename
import os
import imghdr

ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
UPLOAD_PATH = './image'

app = Flask(__name__)
app.config['UPLOAD_PATH'] = UPLOAD_PATH

def allowed_file(_file):
    image_type = imghdr.what(None, _file.read())
    return image_type in ALLOWED_EXTENSIONS

@app.route('/image/<image_name>', methods=['GET'])
def get_image(image_name):
    if image_name is not None:
        try:
            image_name = secure_filename(image_name)
            image = open(os.path.join(app.config['UPLOAD_PATH'], image_name))

            return send_file(image)
        except:
            return 'berhasil'
    else:
        return 'error'

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        _file = request.files['file']
        if _file and allowed_file(_file):
            filename = secure_filename(_file.filename)
            # because imghdr.what() reads file to end, must set file's position 0.
            _file.seek(0)
            try:
                _file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            except IOError:
                os.mkdir(app.config['UPLOAD_PATH'])
                _file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

            return redirect('/image/' + filename)
        else:
            return "Upload failed."
    else:
        return '<form action="." method="post" enctype="multipart/form-data"><input type="file" name="file" /><button type="submit">Upload</button></form>'

if __name__ == '__main__':
    app.run()