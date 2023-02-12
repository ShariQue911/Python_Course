import requests
from urllib import request
import os


def _strip_excess(dict_to_sort, count):
    """
    This strips excess info from response (leaves URI of photo, likes and size)

    :param dict_to_sort:
    :return: dict with likes and photo's URI
    """
    result = dict()
    for pos, values in enumerate(dict_to_sort):
        temp_dict = dict()
        temp_dict['date'] = values['date']
        temp_dict['photo'] = values['sizes'][-1]['type'], values['sizes'][-1]['url']
        temp_dict['likes'] = values['likes']['count']
        result[pos] = temp_dict
        if pos >= (count - 1):
            break
    return result


class VK:
    """
    Class for working with Vkontakte API
    """
    token = 'vk1.a.Ojcz2TapvQy_x6LArQ0uutDVRhj8TOB_3pTpozy0DqgcM1kMGvPfwoJe8D-vUYaGKCjOixEOVdDs9T-3H60O0ceDDE8RHetvcK7CJeLcHqAdr1mqHEaU4daggTOuU8sI0LadrM4pVYO8IYf3w-Z0T3YoP0lka0amiW91RNRhFxZP1WcvV08t99gH6Cwf7ZOp7i-zXmy5IKLa1BjK5px_EA'
    main_url = 'https://api.vk.com/method/'

    def get_photos(self, vk_id, album_id):
        """
        Gets all photos from public profile

        :param album_id: Album ID of VK profile (profile or wall)
        :param vk_id: VK user ID
        :return: dict with likes and photo URLs
        """
        url = self.main_url + 'photos.get/'
        album_name = str()
        params = {
            'owner_id': 221301720,
            'album_id': album_id,
            'extended': '1',
            'photo_sizes': '1',
            'access_token': self.token,
            'v': '5.131'

        }
        if album_id == 'profile':
            album_name = 'профиль'
        elif album_id == 'wall':
            album_name = 'стена'

        response = requests.get(url=url, params=params).json()
        amount = response['response']['count']
        print(f'\nПолучено {amount} фотографий ({album_name}) пользователя ВКонтакте\n')
        while True:
            cmd_param = int(input(f'Сколько фотографий нужно загрузить? (1-{amount}) '))
            if cmd_param <= 0 or cmd_param > amount:
                print('Некорректное количество, введите снова')
            else:
                break
        dict_res = _strip_excess(response['response']['items'], cmd_param)
        print(f'Получено: {cmd_param} фото Вконтакте\n')
        return dict_res
