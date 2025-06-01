from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/posters'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # max 5MB upload

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        file = request.files.get('poster')

        if not movie_name:
            return "Please enter a movie name!"
        if not file or file.filename == '':
            return "Please upload a poster image!"
        if not allowed_file(file.filename):
            return "Allowed image types are png, jpg, jpeg, gif."

        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        return redirect(url_for('result', movie=movie_name, filename=filename))

    return render_template('index.html')

@app.route('/result')
def result():
    movie = request.args.get('movie')
    filename = request.args.get('filename')
    return render_template('result.html', movie=movie, filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
