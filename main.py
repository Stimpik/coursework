from YA import Yandex, ya_token


def main():
    ya.upload_files_to_folder()


if __name__ == '__main__':
    ya = Yandex(ya_token)
    main()
