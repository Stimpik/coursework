import requests
from settings import YA_TOKEN
import json
from tqdm import tqdm
import Vkontakte

ya_token = YA_TOKEN


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
        fotos = Vkontakte.vk.create_data_dict()
        folder = self.create_folder()
        headers = {'Authorization': f'OAuth {ya_token}'}
        uri = 'v1/disk/resources/upload'
        result_json = []
        upload_file_params = {'path': f'{folder}/data.json'}
        for foto in tqdm(fotos, desc='Подождите, идет загрузка фото на диск', unit=' Photo'):
            params = {'path': f"{folder}/{foto['name']}.jpg", 'url': foto['url']}
            requests.post(self.base_url + uri, headers=headers, params=params)
            json_dict = {'file_name': foto['name'],
                         'size': foto['size']}
            result_json.append(json_dict)
        with open("photo_data.json", 'w') as file:
            json.dump(result_json, file)
        upload_response = requests.get(self.base_url + uri, headers=headers, params=upload_file_params)
        requests.put(upload_response.json()['href'], data=open('photo_data.json', 'rb'), headers=headers)
        print('Готово!')
