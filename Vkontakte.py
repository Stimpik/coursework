import requests
from datetime import datetime
from settings import TOKEN

access_token = TOKEN


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
                    photo_dict['name'] = str(photo_dict['name']) + datetime.utcfromtimestamp(item['date']).strftime(
                        '-%Y-%m-%d')
            data_dict.append(photo_dict)
            acc += 1

        return data_dict


vk = VK(access_token)
