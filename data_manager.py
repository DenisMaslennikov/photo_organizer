import orjson
import os


def load_settings(path: str) -> dict[str, list[str]]:
    """Load settings from file."""
    settings: dict[str, list[str]] = {}
    try:
        with open(path, 'rb') as db:
            return orjson.loads(db.read())
    except FileNotFoundError:
        print('Не удалось загрузить файл настроек. Использованы значения по '
              'умолчанию')
        settings['extensions'] = ['.png', '.gif', '.jpeg', '.jpg', '.bmp']
        settings['folders'] = ['test_img']
        settings['photo_db'] = []
    return settings


def save_settings(path: str, settings: dict[str, list[str]]) -> None:
    """Save setting to file."""
    with open(path, 'wb') as db:
        db.write(orjson.dumps(settings))


def load_image_db(path: str) -> list[dict[str, list[str]]]:
    """Load image data base from file."""
    image_db: list[dict[str, list[str]]] = {}
    try:
        with open(path, 'rb') as db:
            return orjson.loads(db.read())
    except FileNotFoundError:
        print('Не удалось загрузить базу изображений')
        return image_db


def save_image_db(path: str, image_db: list[dict[str, list[str]]]) -> None:
    """Save image data base to file."""
    with open(path, 'wb') as db:
        db.write(orjson.dumps(image_db))


def scan_folders(folders: list[str],
                 extensions: list[str],
                 image_db: dict[str, list[str]],
                 ) -> tuple[dict[str, dict[str, list[str]]],
                            dict[str, list[str]]]:
    """Scan selected folders."""
    copy_image_db: dict[str, dict[str, list[str]]] = {}
    collect_images: list[tuple[str, str]] = []
    for folder in folders:
        if os.path.isdir(folder):
            for path, dirs, files in os.walk(folder):
                for file in files:
                    if os.path.splitext(file)[-1] in extensions:
                        collect_images.append((os.path.abspath(path), file))
        else:
            print(f'Каталог {folder} не найден')

    for new_image in collect_images:
        key = os.path.join(new_image[0], new_image[1])
        values = image_db.get(key)

        if values:
            copy_image_db[key] = values
        else:
            copy_image_db[key] = {'tags': [os.path.split(new_image[0])[-1]]}

    tags_db = generate_tags(copy_image_db)
    return copy_image_db, tags_db


def generate_tags(image_db: dict[str, list[str]]) -> dict[str, list[str]]:
    tags_db: dict[str, list[str]] = {}
    for path, values in image_db.items():
        for tag in values['tags']:
            if tags_db.get(tag):
                tags_db[tag].append(path)
            else:
                tags_db[tag] = [path]
    return tags_db
