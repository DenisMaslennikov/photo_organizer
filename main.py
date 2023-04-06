import data_manager as dm
import menu

settings_path: str = "settings.json"
data_path: str = 'photo_db.json'

main_db: dict[str, dict[str, list[str]]] = {}
tags_db: dict[str, list[str]]


settings: dict[str, list[str]] = {}


def main():
    """Main function."""
    global main_db
    global settings
    global tags_db
    menu.greetings()
    print()
    settings = dm.load_settings(settings_path)
    main_db = dm.load_image_db(data_path)

    select_option: str = ''
    while select_option != '0':
        print()
        print('1. Управление каталогами')
        print('2. Управление расширениями')
        print('3. Сканировать каталоги')
        print('4. "Работа" с изображениями')
        print('5. Сохранить настройки')
        print('6. Сохранить базу тегов')

        print('0. Выход')

        select_option = input()
        match select_option:
            case '1':
                settings['folders'] = menu.manage_folders(settings['folders'])

            case '2':
                settings['extensions'] = menu.manage_extensions(
                    settings['extensions'])
            case '3':
                main_db, tags_db = dm.scan_folders(settings['folders'],
                                                   settings['extensions'],
                                                   main_db)
            case '4':
                menu.image_process(main_db, in_place=True)
            case '5':
                dm.save_settings(settings_path, settings)
            case '6':
                dm.save_image_db(data_path, main_db)


if __name__ == '__main__':
    main()
