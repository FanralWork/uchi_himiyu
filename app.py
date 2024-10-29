from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import subprocess
import create_thumbnails

app = Flask(__name__)

VIDEO_DIR = 'videos'
THUMBNAIL_DIR = 'static/thumbnails'
ALLOWED_EXTENSIONS = {'mp4','jpg'}


# Проверка расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/videos/<int:class_number>/<path:video_name>')
def serve_video(class_number, video_name):
    return send_from_directory(f'videos/{class_number}', video_name)

# Маршрут для проигрывания видео
# @app.route('/play/<int:class_number>/<video_name>')
# def play_video(class_number, video_name):
#     video_path = os.path.join(VIDEO_DIR, str(class_number))
#     return render_template('player.html', class_number=class_number, video_name=os.path.splitext(os.path.basename(video_name))[0])

@app.route('/play/<int:class_number>/<video_name>')
def play_video(class_number, video_name):
    # Параметры like_count и dislike_count могут браться из базы данных или других источников
    like_count = 0
    dislike_count = 0
    return render_template(
        'player.html',
        class_number=class_number,
        video_name=video_name,
        like_count=like_count,
        dislike_count=dislike_count
    )


# Маршрут для загрузки видео
@app.route('/upload', methods=['GET', 'POST'])
def upload_video():
    if request.method == 'POST':
        class_number = request.form['class_number']
        file = request.files['file']
        thumbnail_option = request.form['thumbnail_option']
        thumbnail = request.files.get('thumbnail')

        # Сохранение видеофайла
        if file and allowed_file(file.filename):
            class_folder = os.path.join(VIDEO_DIR, class_number)
            os.makedirs(class_folder, exist_ok=True)
            video_path = os.path.join(class_folder, file.filename)
            file.save(video_path)

        # Если пользователь выбрал автоматическое создание превью
        if thumbnail_option == 'auto':
            thumbnail_name = os.path.splitext(os.path.basename(video_path))[0] + ".jpg"
            thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_name)
            create_thumbnails.create_thumbnail(video_path, thumbnail_path)
        elif thumbnail_option == 'manual' and thumbnail and allowed_file(thumbnail.filename):
            # Пользователь выбрал загрузить своё превью
            thumbnail_name = os.path.splitext(file.filename)[0] + ".jpg"
            thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_name)
            print(thumbnail_name, thumbnail_path)
            thumbnail.save(thumbnail_path)
        else:
            thumbnail_name = os.path.splitext(os.path.basename(video_path))[0] + ".jpg"
            thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_name)
            create_thumbnails.create_thumbnail(video_path, thumbnail_path)

        return redirect(url_for('index'))

    return render_template('upload.html')


# API для получения списка видео
@app.route('/api/videos/<int:class_number>')
def api_videos(class_number):
    class_path = os.path.join(VIDEO_DIR, str(class_number))
    videos = [f for f in os.listdir(class_path) if f.endswith('.mp4')]
    video_data = [{"name": os.path.splitext(f)[0], "thumbnail": f"{os.path.splitext(f)[0]}.jpg"} for f in videos]
    return jsonify(video_data)


if __name__ == '__main__':
    app.run(debug=True)