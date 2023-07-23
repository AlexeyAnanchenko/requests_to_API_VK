import os
import csv
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


def write_to_csv(data):
    """Функция для записи итогов в csv-файл"""

    file_name = "results.csv"

    with open(file_name, mode='w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)


if __name__ == '__main__':
    cnt_posts = get_posts()
    data = [
        ['Метрики по группе', 'Количество'],
        ['Подписчиков', get_members()],
        ['Постов', cnt_posts],
        ['Репостов', get_reposts(cnt_posts)]
    ]
    write_to_csv(data)
