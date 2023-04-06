import os.path
from copy import deepcopy


def print_numerated_list(printing_list: list):
    """Printing numerated list, start from 1."""
    for index, item in enumerate(printing_list):
        print(f'{index + 1: >3}. {item}')


def greetings() -> None:
    """Print greetings."""
    print('Приветствую юный и неосторожный %username% я помогу тебе '
          'организовать твои картинки!')


def manage_folders(folders: list[str]) -> list[str]:
    """Image folders management."""
    copy_folders = folders.copy()
    select_option: str = ''
    while select_option != '0':
        print()
        print('Выбранные каталоги для мониторинга:', *copy_folders, sep='\n')
        print()

        print('1. Добавить каталог')
        print('2. Удалить каталог')

        print('0. Вернутся в предыдущее меню')

        select_option = input()

        match select_option:

            case '1':
                user_choose: str = ''
                while user_choose != '0':
                    user_choose = input('Введите новый каталог. 0 для '
                                        'выхода: ').lower()
                    new_folder = os.path.abspath(user_choose)
                    if (os.path.isdir(new_folder)):
                        if (new_folder not in copy_folders):
                            copy_folders.append(new_folder)
                            print(f'Добавлен каталог {new_folder}')
                        else:
                            print(f'Каталог {new_folder} уже добавлен')
                    else:
                        print('Каталог не существует.')

            case '2':
                del_me = -1
                while del_me != 0:
                    print_numerated_list(copy_folders)
                    try:
                        del_me = int(input('Введите номер каталога который '
                                           'надо удалить. 0 для выхода: '))
                        if del_me > 0:
                            del copy_folders[del_me - 1]
                        else:
                            raise IndexError
                    except IndexError:
                        print('Введен неправильный номер. Попробуйте снова.')
                    except ValueError:
                        print('Введено неправильное значение. Введите число.')

    return copy_folders


def manage_extensions(extensions: list[str]) -> list[str]:
    """Image extensions management."""
    copy_extensions = extensions.copy()
    select_option: str = ''
    while select_option != '0':
        print()
        print('Выбранные расширения файлов:', *copy_extensions, sep='\n')
        print()

        print('1. Добавить расширение')
        print('2. Удалить расширение')

        print('0. Вернутся в предыдущее меню')

        select_option = input()

        match select_option:

            case '1':
                new_extension: str = ''
                while new_extension != '0':
                    new_extension = input('Введите новое расширение. 0 для '
                                          'выхода: ').lower()
                    if (new_extension not in copy_extensions
                            and new_extension != '0'):
                        if (new_extension.startswith('.')
                                and len(new_extension) > 1):
                            copy_extensions.append(new_extension.lstrip('.'))
                            print(f'Добавлено расширение {new_extension}')
                        else:
                            print('Введено неправильное значение. Расширение '
                                  'должно начинаться с "." и содержать '
                                  'минимум 2 символа')
                    elif new_extension == '0':
                        pass
                    else:
                        print(f'Расширение {new_extension} уже добавлено')

            case '2':
                del_me = -1
                while del_me != 0:
                    print_numerated_list(copy_extensions)
                    try:
                        del_me = int(input('Введите номер расширения которое '
                                           'надо удалить. 0 для выхода: '))
                        if del_me > 0:
                            del copy_extensions[del_me - 1]
                        else:
                            raise IndexError
                    except IndexError:
                        print('Введен неправильный номер. Попробуйте снова.')
                    except ValueError:
                        print('Введено неправильное значение. Введите число.')

    return copy_extensions


def image_process(image_db: dict[str, dict[str, list[str]]],
                  in_place: bool = False
                  ) -> dict[str, dict[str, list[str]]]:
    """Image management. View, remove/add tags."""
    if in_place:
        copy_image_db = image_db
    else:
        copy_image_db = deepcopy(image_db)

    select_option: str = ''
    while select_option != '0':
        print()
        print('1. "Просмотр" изображений')
        print('2. "Просмотр" изображений по тегу')
        print('3. Массовое добавление тега')
        print('0. Вернутся в предыдущее меню')
        select_option = input()
        match select_option:
            case '1':
                show_images(copy_image_db)
            case '2':
                tag = input('Введите тег для просмотра: ')
                show_images(copy_image_db, tag)
            case '3':
                show_images(copy_image_db, only_show=True)
                tag = input('Введите тег: ')
                try:
                    images_index = list(map(int, input('Введите номера '
                                                       'изображений через '
                                                       'пробел: ').split()))
                except ValueError:
                    print('Введено неправильное значение. Введите только '
                          'числа через пробел.')
                else:
                    images_index.sort()
                    current_index = 0
                    for index, image in enumerate(image_db):
                        if index == images_index[current_index] - 1:
                            image_db[image]['tags'].append(tag)
                            if len(images_index) > current_index + 1:
                                current_index += 1
                            else:
                                break


def show_images(image_db: dict[str, dict[str, list[str]]],
                tag: str = None,
                only_show: bool = False) -> None:
    """Print numerated images list."""
    select_option: str = ''
    max_index: int = 0
    while select_option != '0':
        for index, image in enumerate(image_db):
            max_index = index + 1
            if tag in image_db[image]['tags'] or not tag:
                print(f'{index + 1: >3}. {image} '
                      f'\n Tags: {*image_db[image]["tags"],}')

        if not only_show:
            select_option = input('Введите номер изображения. 0 для выхода: ')
            try:
                if 0 < int(select_option) <= max_index:
                    for index, image in enumerate(image_db):
                        if index == int(select_option) - 1:
                            manage_image_tags(image, image_db[image]['tags'],
                                              in_place=True)
                            break
                elif '0' == select_option:
                    pass
                else:
                    raise IndexError()

            except IndexError:
                print('Введен неправильный номер. Попробуйте снова')
            except ValueError:
                print('Введено неправильное значение. Введите число.')
        else:
            select_option = '0'


def manage_image_tags(image: str, tags: list, in_place: bool = False) -> dict:
    """Add/remove tags for single image."""
    if in_place:
        copy_tags = tags
    else:
        copy_tags = tags.copy()
    select_option: str = ''
    while select_option != '0':
        print('Выбранное изображение:')
        print(f'{image} '
              f'\nTags: {*copy_tags,}')
        print()
        print('1. Добавить тег')
        print('2. Удалить тег')
        print('3. Удалить все теги')
        print('0. Вернутся в предыдущее меню')
        select_option = input()
        match select_option:
            case '1':
                new_tag = ''
                while new_tag != '0':
                    new_tag = input('Введите тег. 0 для выхода: ')
                    if (new_tag not in copy_tags
                            and new_tag != '0'
                            and new_tag != ''):
                        copy_tags.append(new_tag)
                        print(f'Добавлен тег {new_tag}')
                    elif new_tag == '0' or new_tag == '':
                        pass
                    else:
                        print(f'Тег {new_tag} уже добавлен')
            case '2':
                del_me = ''
                while del_me != 0:
                    print_numerated_list(copy_tags)
                    try:
                        del_me = int(input('Введите номер тега который '
                                           'надо удалить. 0 для выхода: '))
                        if del_me > 0:
                            del copy_tags[del_me - 1]
                        else:
                            raise IndexError
                    except IndexError:
                        print('Введен неправильный номер. Попробуйте снова.')
                    except ValueError:
                        print('Введено неправильное значение. Введите число.')

            case '3':
                copy_tags = []
    return copy_tags
