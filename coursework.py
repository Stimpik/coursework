from tqdm import tqdm
from settings import TOKEN, YA_TOKEN
import requests
from datetime import datetime
import json


class VK:

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_user_id(self, id):

        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': id}
        response = requests.get(url, params={**self.params, **params})
        for ids in response.json()['response']:
            return ids['id']

    def get_photo_date(self):
        try:
            id = input('Введите ID пользователя: ')
            count = int(input('Введите количество фотографий (по умолчанию 5): ') or 5)
            album_id = input('Введите id альбома (по умолчанию "profile"): ') or 'profile'
            if not isinstance(id, int):
                id = self.get_user_id(id)
            url = 'https://api.vk.com/method/photos.get'
            params = {'owner_id': id, 'album_id': album_id, 'extended': 1, 'photo_sizes': 1, 'count': count, "rev": 1}
            respone = requests.get(url, params={**self.params, **params})
            return respone.json()['response']['items']
        except:
            print('Не удалось найти альбом, попробуйте снова.')
            return self.get_photo_date()


    def create_data_dict(self):

        data_dict = []
        for photo in self.get_photo_date():
            photo_dict = {'name': photo['likes']['count'],
                          'date': photo['date'],
                          'size': photo['sizes'][-1]['type'],
                          'url': photo['sizes'][-1]['url']}
            acc = 0
            for item in data_dict:
                if photo_dict['name'] == item['name']:
                    photo_dict['name'] = str(photo_dict['name']) + datetime.utcfromtimestamp(item['date']).strftime('-%Y-%m-%d')
            data_dict.append(photo_dict)
            acc += 1

        return data_dict


class Yandex:
    base_url = 'https://cloud-api.yandex.net:443/'

    def __init__(self, ya_token):
        self.ya_token = ya_token

    def create_folder(self):
        directory_name = input('Введите название папки для ЯндесДиска: ')
        headers = {'Authorization': f'OAuth {ya_token}'}
        uri = 'v1/disk/resources/'
        params = {'path': directory_name}
        respone = requests.put(self.base_url + uri, headers=headers, params=params)
        if respone.status_code == 409:
            while True:
                folder = input('Такая папка уже существует, придумайте другое имя, для отмены введите "N": ')
                if folder.lower() == 'n':
                    break
                else:
                    params = {'path': folder}
                    requests.put(self.base_url + uri, headers=headers, params=params)
                    return folder
        return directory_name

    def upload_files_to_folder(self):
        fotos = vk.create_data_dict()
        folder = self.create_folder()
        headers = {'Authorization': f'OAuth {ya_token}'}
        uri = 'v1/disk/resources/upload'
        result_json = []
        upload_file_params = {'path': f'{folder}/data.txt'}
        for foto in tqdm(fotos, desc='Подождите, идет загрузка фото на диск', unit=' Photo'):
            params = {'path': f"{folder}/{foto['name']}.jpg", 'url': foto['url']}
            requests.post(self.base_url + uri, headers=headers, params=params)
            json_dict = {'file_name': foto['name'],
                         'size': foto['size']}
            result_json.append(json_dict)
        with open("photo_data.txt", 'w') as file:
            json.dump(result_json, file)
        upload_response = requests.get(self.base_url + uri, headers=headers, params=upload_file_params)
        requests.put(upload_response.json()['href'], data=open('photo_data.txt', 'rb'), headers=headers)
        print('Готово!')


def main():
    ya.upload_files_to_folder()

if __name__ == '__main__':
    access_token = TOKEN
    vk = VK(access_token)
    ya_token = YA_TOKEN
    ya = Yandex(ya_token)
    main()