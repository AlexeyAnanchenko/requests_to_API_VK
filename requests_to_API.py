import os
import requests


# импортируем конфиденц. данные о токене из окружения
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

GROUP_ID = '215426617'  # ID группы на выбор
API_VERSION = '5.131'

# параметры, необходимые для любого запроса
params = {
    'access_token': ACCESS_TOKEN,
    'v': API_VERSION
}


def get_response(method):
    """Шаблон запроса к API VK"""

    response = requests.get(
        f'https://api.vk.com/method/{method}',
        params=params
    )
    return response.json()['response']


def get_members():
    """Запрос для получения списка участников"""

    method = 'groups.getMembers'
    params['group_id'] = GROUP_ID
    cnt_members = get_response(method)['count']
    del params['group_id']
    return cnt_members


def get_posts():
    """Запрос для получения количества постов в группе"""

    method = 'wall.get'
    params['owner_id'] = f'-{GROUP_ID}'
    cnt_posts = get_response(method)['count']
    del params['owner_id']
    return cnt_posts


def get_reposts(cnt_posts):
    """Запрос для получения количества репостов в группе"""

    method = 'wall.get'
    params['owner_id'] = f'-{GROUP_ID}'
    params['count'] = 100
    cnt_reposts = 0
    count = 0
    offset = 0

    while cnt_posts != count:
        posts = get_response(method)['items']
        for el in posts:
            cnt_reposts += el['reposts']['count']
            count += 1
        if count < cnt_posts:
            params['offset'] = offset + count
    return cnt_reposts


if __name__ == '__main__':
    cnt_posts = get_posts()
    print(f'Количество подписчиков в группе 1Т Спринт: {get_members()}.')
    print(f'Количество постов в группе 1Т Спринт: {cnt_posts}.')
    print(f'Количество репостов в группе 1Т Спринт: {get_reposts(cnt_posts)}.')
