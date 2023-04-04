import json
import os


def load_settings(path: str) -> dict[str, list[str]]:
    """Load settings from file."""
    settings: dict[str, list[str]] = {}
    try:
        with open(path, 'r') as db:
            return json.load(db)
    except FileNotFoundError:
        print('Не удалось загрузить файл настроек. Использованы значения по '
              'умолчанию')
        settings['extensions'] = ['.png', '.gif', '.jpeg', '.jpg', '.bmp']
        settings['folders'] = ['test_img']
        settings['photo_db'] = []
    return settings


def save_settings(path: str, settings: dict[str, list[str]]) -> None:
    """Save setting to file."""
    with open(path, 'w') as db:
        json.dump(settings, db)


def load_image_db(path: str) -> list[dict[str, list[str]]]:
    """Load image data base from file."""
    image_db: list[dict[str, list[str]]] = {}
    try:
        with open(path, 'r') as db:
            return json.load(db)
    except FileNotFoundError:
        print('Не удалось загрузить базу изображений')
        return image_db


def save_image_db(path: str, image_db: list[dict[str, list[str]]]) -> None:
    """Save image data base to file."""
    with open(path, 'w') as db:
        json.dump(image_db, db)


def scan_folders(folders: list[str],
                 extensions: list[str],
                 image_db: list[dict[str, list[str]]]
                 ) -> list[dict[str, list[str]]]:
    """Scan selected folders."""
    copy_image_db: list[dict[str, list[str]]] = []
    collect_images: list[tuple[str, str]] = []
    for folder in folders:
        if os.path.isdir(folder):
            for path, dirs, files in os.walk(folder):
                for file in files:
                    for extension in extensions:
                        if extension in file:
                            collect_images.append((path, file))
        else:
            print(f'Каталог {folder} не найден')

    if image_db:
        for new_image in collect_images:
            already_have = False
            for image in image_db:
                if (image['path'] == new_image[0]
                        and image['file'] == new_image[1]):
                    copy_image_db.append({
                        'path': image['path'],
                        'file': image['file'],
                        'tags': image['tags'],
                    })
                    already_have = True

            if not already_have:
                copy_image_db.append({
                    'path': new_image[0],
                    'file': new_image[1],
                    'tags': [new_image[0].split('\\')[-1]],
                })

    else:
        for new_image in collect_images:
            copy_image_db.append({
                'path': new_image[0],
                'file': new_image[1],
                'tags': [new_image[0].split('\\')[-1]],
            })

    return copy_image_db
