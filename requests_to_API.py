import os
import csv
import requests
import copy
import time
from datetime import datetime as dt, timedelta as td


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


def get_count_posts():
    """Запрос для получения количества постов в группе"""

    method = 'wall.get'
    params['owner_id'] = f'-{GROUP_ID}'
    params['count'] = 1  # выгрузим минимум постов
    cnt_posts = get_response(method)['count']
    del [params['owner_id'], params['count']]
    return cnt_posts


def get_posts(cnt_posts):
    """Запрос на получение всех постов"""

    method = 'wall.get'
    params['owner_id'] = f'-{GROUP_ID}'
    params['count'] = 100
    count = 0
    offset = 0

    # переберём все посты и оставим только нужную информацию по каждому
    # посту в виде списка словарей
    posts = []

    while cnt_posts != count:
        posts_json = get_response(method)['items']

        for el in posts_json:
            posts.append({
                'id': el['id'],
                'date': dt.fromtimestamp(el['date']).date(),
                'text': el['text'][:50].replace('\n', ' ') + '...',
                'likes': el['likes']['count'],
                'comments': el['comments']['count'],
                'reposts': el['reposts']['count']
            })
            count += 1

        if count < cnt_posts:
            params['offset'] = offset + count

    del [params['count'], params['offset'], params['owner_id']]
    return posts


def get_reposts(posts):
    """Запрос для получения количества репостов в группе"""

    cnt_reposts = 0
    for el in posts:
        cnt_reposts += el['reposts']
    return cnt_reposts


def groups_data(cnt_posts, posts):
    """Собирает данные по группе в нужный формат для записи в csv"""

    metrics_dict = {
        'Подписчиков': get_members(),
        'Постов': cnt_posts,
        'Репостов': get_reposts(posts)
    }
    data = []
    for metrics, val in metrics_dict.items():
        data.append({
            'Метрики по группе': metrics,
            'Количество': val
        })
    return data


def get_posts_by_likes(posts):
    """возвращает данные на ТОП 10 постов по лайкам"""
    posts_filter = []

    # нам нужны только посты за последние 3 месяца
    start_date = (dt.now() - td(days=90)).date()
    for el in posts:
        if el['date'] >= start_date:
            del [el['reposts'], el['comments']]
            posts_filter.append(el)

    # найдём ТОП 10 постов по лайкам
    posts_filter = sorted(
        posts_filter,
        key=lambda el: el['likes'],
        reverse=True
    )[:10]

    return posts_filter


def get_posts_by_comments(posts):
    """Возвращает данные на ТОП 10 постов по комментам"""

    posts_sort = sorted(
        posts,
        key=lambda el: el['comments'],
        reverse=True
    )[:10]

    # подготовим данные для записи в csv
    for el in posts_sort:
        del [el['reposts'], el['likes']]

    return posts_sort


def get_comments(posts):
    """возвращает данные с комментариями к постам для записи в csv"""

    # нам нужны только те комментарии по постам в которых есть слово ниже
    sample = 'Data Engineering'

    # сюда будем собирать строки для csv в виде списка словарей
    data = []

    # определим функцию для добавления данных в список выше
    def add_comment_to_list(obj):
        if sample.lower() in obj['text'].lower():
            data.append({
                'id_post': post['id'],
                'date_post': post['date'],
                'text_post': post['text'],
                'id_comment': obj['id'],
                'date': dt.fromtimestamp(obj['date']).date(),
                'text': obj['text'],
                'author_id': obj['from_id']
            })

    # будем запрашивать комментарии по каждому посту и с учётом тредов
    method = 'wall.getComments'
    params['owner_id'] = f'-{GROUP_ID}'
    params['count'] = 100
    params['thread_items_count'] = 10
    for post in posts:
        params['post_id'] = post['id']
        cnt_comments = post['comments']
        count = 0
        offset = 0

        while cnt_comments != count:
            comments_json = get_response(method)['items']
            # делаем небольшой перерыв между запросами, иначе блокируют
            time.sleep(1)

            for obj in comments_json:
                add_comment_to_list(obj)
                count += 1

                # у некоторых комментариев есть треды, которые входят
                # в общее кол-во комментариев поста
                thread_count = 0
                while thread_count != obj['thread']['count']:

                    for thread in obj['thread']['items']:
                        add_comment_to_list(thread)
                        thread_count += 1

                count += thread_count

            if count < cnt_comments:
                params['offset'] = offset + count
    return data


def write_to_csv(data, file_name):
    """Функция для записи итогов в csv-файл"""

    with open(file_name, mode='w', encoding='utf-8') as file:
        fields = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()  # записали заголовки

        # теперь строки
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    # задания 1-3
    cnt_posts = get_count_posts()
    posts = get_posts(cnt_posts)
    write_to_csv(
        data=groups_data(cnt_posts, posts),
        file_name="results_1-3.csv"
    )

    # задание 4
    data_likes = get_posts_by_likes(copy.deepcopy(posts))
    write_to_csv(data=data_likes, file_name="results_4.csv")

    # задание 5
    data_comments = get_posts_by_comments(copy.deepcopy(posts))
    write_to_csv(data=data_comments, file_name="results_5.csv")

    # задание 6
    comments = get_comments(posts)
    write_to_csv(data=comments, file_name="results_6.csv")
