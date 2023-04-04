import data_manager as dm
import menu

settings_path: str = "settings.json"
data_path: str = 'photo_db.json'

main_db: list[dict[str, list[str]]] = []
settings: dict[str, list[str]] = {}


def main():
    """Main function."""
    global main_db
    global settings
    menu.greetings()
    print()
    settings = dm.load_settings(settings_path)
    main_db = dm.load_image_db(data_path)

    select_option: str = ''
    while select_option != '0':
        menu.print_main_menu()
        select_option = input()
        match select_option:
            case '1':
                settings['folders'] = menu.manage_folders(settings['folders'])

            case '2':
                settings['extensions'] = menu.manage_extensions(
                    settings['extensions'])
            case '3':
                main_db = dm.scan_folders(settings['folders'],
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
