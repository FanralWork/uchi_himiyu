import os
import subprocess

# Укажите путь к папке с видео и папке для превью
VIDEO_DIR = 'videos'
THUMBNAIL_DIR = 'static/thumbnails'


# Функция для создания превью из середины видео
def create_thumbnail(video_path, thumbnail_path):
    # Укажите полный путь к ffprobe
    # ffprobe_path = r"ffmpeg\bin\ffprobe.exe"
    cmd_duration = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{video_path}"'
    result = subprocess.run(cmd_duration, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Проверяем, успешно ли выполнена команда
    if result.returncode != 0:
        try:
            error_message = result.stderr.decode('utf-8', errors='replace').strip()
        except UnicodeDecodeError:
            error_message = result.stderr.decode('cp1251', errors='replace').strip()

        print(f"Ошибка при получении длительности видео для {video_path}: {error_message}")
        return

    # Преобразуем длительность видео в секунды
    duration_str = result.stdout.decode('utf-8', errors='replace').strip()

    if not duration_str:
        print(f"Не удалось получить длительность для {video_path}")
        return

    # Преобразуем строку в число
    try:
        total_seconds = float(duration_str)
    except ValueError:
        print(f"Не удалось преобразовать длительность для {video_path}: {duration_str}")
        return

    # Находим середину видео
    midpoint = total_seconds / 2

    # Формируем команду FFmpeg для создания превью
    cmd = f'ffmpeg -ss {midpoint} -i "{video_path}" -vframes 1 -q:v 2 "{thumbnail_path}"'

    print(f"Создание превью для {video_path} в {thumbnail_path}...")
    print(f"Команда: {cmd}")

    # Запускаем команду FFmpeg
    ffmpeg_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if ffmpeg_result.returncode != 0:
        try:
            error_message = ffmpeg_result.stderr.decode('utf-8', errors='replace').strip()
        except UnicodeDecodeError:
            error_message = ffmpeg_result.stderr.decode('cp1251', errors='replace').strip()

        print(f"Ошибка при создании превью: {error_message}")
    else:
        print(f"Превью успешно создано: {thumbnail_path}")


# Функция для обработки всех видео в папке
def process_videos():
    # Создаем папку для превью, если она не существует
    if not os.path.exists(THUMBNAIL_DIR):
        os.makedirs(THUMBNAIL_DIR)

    for root, dirs, files in os.walk(VIDEO_DIR):
        for file in files:
            if file.endswith('.mp4'):
                video_path = os.path.join(root, file)
                # Имя превью будет такое же, как у видео, но сохраняем в THUMBNAIL_DIR
                thumbnail_name = os.path.splitext(file)[0] + ".jpg"
                thumbnail_path = os.path.join(THUMBNAIL_DIR, thumbnail_name)
                create_thumbnail(video_path, thumbnail_path)


if __name__ == "__main__":
    process_videos()