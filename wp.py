# TODO: Implement tests.

import os
import requests
from dotenv import load_dotenv, find_dotenv

dotenv_file = find_dotenv()
load_dotenv(dotenv_file)


WORDPRESS_MEDIA_URL = os.getenv('WORDPRESS_MEDIA_URL')
WORDPRESS_GET_MEDIA_URL = os.getenv('WORDPRESS_GET_MEDIA_URL')
WORDPRESS_ACCESS_TOKEN = os.getenv('WORDPRESS_ACCESS_TOKEN')
WORDPRESS_HEADER = {'Authorization': f'BEARER {WORDPRESS_ACCESS_TOKEN}'}


def upload_media_to_wordpress(raw_data):
    image_name = raw_data.filename
    with open(image_name, 'rb') as img:
        payload = {}
        files = [('media', (image_name, img, 'application/octet-stream'))]

        response = requests.post(WORDPRESS_MEDIA_URL, data=payload, files=files, headers=WORDPRESS_HEADER)

        print('Compressing and sending data...')
        print(response.status_code)
        return response


def upload_multiple_media_to_wordpress(collection):
    images = []
    for raw_data in collection:
        images.append(upload_media_to_wordpress(raw_data))

    return images


def get_wordpress_media():
    response = requests.get(WORDPRESS_GET_MEDIA_URL, headers=WORDPRESS_HEADER)
    media_dict = response.json()["media"]
    media_list = []

    for media in media_dict:
        media_list.append(media)
        print(f"{media['ID']}=> file: {media['file']}, url: {media['URL']}")

    return media_list
