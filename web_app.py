import os
from flask import Flask, request, redirect, send_file, render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
UPLOAD_FOLDER = '/files'


app = Flask(__name__, template_folder='templates', static_folder="static")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if os.environ.get(username) == password:
        return username


@app.route('/', methods=['GET'])
@auth.login_required
def index_page():
    files = os.listdir(UPLOAD_FOLDER)
    user = auth.current_user()
    return render_template('index.html', files=files,
                           folder=UPLOAD_FOLDER, username=user)


@app.route('/upload_file', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    if request.method == ['POST']:
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(f"saved file {file} successfully")
            return redirect('/')


@app.route('/download_file/<filename>')
@auth.login_required
def download_file(filename):
    file_path = f'{UPLOAD_FOLDER}/{filename}'
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
