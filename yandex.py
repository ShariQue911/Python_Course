import requests
import json
from datetime import datetime


class Yandex:
    """
    Class for working with Yandex API
    """
    def __init__(self, token):
        self.token = token

    directory = '/API_IMG/'

    log_file = 'yandex_logs.txt'
    open(log_file, 'w')

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth ' + self.token
        }
        with open(log_file,'a') as f:
            f.write(now.strftime("%d%m%Y %H:%M:%S")+'\n')

    def check_photo(self, path):
        """
        Checks if photo with specified name exists on remote folder

        :param path: file URL to check
        :return: boolean True (if exists) of False (if doesn't exists)
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self._get_headers()
        params = {'path': path}
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False

    def upload_to_disk(self, remote_file_path, ext_url):
        """
        This sends a POST request to a remote folder
        :param remote_file_path: path to a remote folder
        :param ext_url: external URL to upload
        :return: response from server
        """
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self._get_headers()
        params = {
            "path": remote_file_path,
            'url': ext_url,
            "overwrite": "true"
        }
        response = requests.post(url=url, headers=headers, params=params)
        return response

    def upload_urls_vk(self, info_dict):
        print('Начинаю загрузку на Яндекс.Диск...')
        with open('filedata_yandex.json', 'w') as file:
            counter = 1
            data = dict()
            for items, content in info_dict.items():
                print(items)
                print(content)
                yan_path = str()
                vk_url = str()
                filename = str(content['likes']) + '.jpg'
                yan_path = self.directory + filename
                vk_url = content['photo'][-1]
                date = content['date']                # this sets photo's date from metadata
                is_exist = self.check_photo(yan_path)
                if is_exist is False:
                    print('yan_path: '+yan_path)
                    print(vk_url)
                    response = self.upload_to_disk(yan_path, vk_url)
                    print(response)
                    if response.status_code == 202:
                        print(f'Файл {filename} загружен на Яндекс.Диск в папку {self.directory.replace("/", "")}\n')
                elif is_exist is True:
                    # date = str(datetime.now())       //this sets current system date
                    # date = date.replace(':', '_')
                    filename = f'{content["likes"]}__{date}.jpg'
                    yan_path = self.directory + filename
                    response = self.upload_to_disk(yan_path, vk_url)
                    if response.status_code == 202:
                        print(f'Файл {filename} загружен на Яндекс.Диск')
                data[counter] = {'filename': filename, 'size': content['photo'][0]}
                counter += 1
            json.dump(data, file, indent=4)
            print('Загрузка на Яндекс.Диск завершена.')
            with open(log_file,'a') as f:
                f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+': '+'Загрузка на Яндекс.Диск завершена.'+'\n')



log_file = 'yandex_logs.txt'
open(log_file, 'w')
with open(log_file,'a') as f:
    f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S")+'\n')