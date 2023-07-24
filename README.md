# requests_to_API_VK
Задание на получение данных с API VK в рамках курса "Инженер Данных"

Для работы скрипта необходимо добавить переменную окружения ACCESS_TOKEN - токен VK для взаимодействия с API VK

- Скрипт задания расположен по пути: <code>[.requests_to_API.py](https://github.com/AlexeyAnanchenko/requests_to_API_VK/blob/main/requests_to_API.py)</code>.


### Результаты отработки скрипта представлены в файлах ниже:

- Задания с 1 по 3: <code>[./results/results_1-3.csv](https://github.com/AlexeyAnanchenko/requests_to_API_VK/blob/main/results/results_1-3.csv)</code>.
- Задание 4: <code>[./results/results_4.csv](https://github.com/AlexeyAnanchenko/requests_to_API_VK/blob/main/results/results_4.csv)</code>.
- Задание 5: <code>[./results/results_5.csv](https://github.com/AlexeyAnanchenko/requests_to_API_VK/blob/main/results/results_5.csv)</code>.
- Задание 6: <code>[./results/results_6.csv](https://github.com/AlexeyAnanchenko/requests_to_API_VK/blob/main/results/results_6.csv)</code>.

### Условия задач:

Используя API VK, проанализировать группу по следующим характеристикам:

1. Количество постов в группе.
2. Количество подписчиков в группе.
3. Количество репостов в группе.
4. Найти TOP 10 самых популярных новостей за последние 3 месяца (популярность новости определяется количеством лайков). Вывести новость и количество лайков.
5. Найти TOP 10 постов с комментариями (выводятся посты с максимальным количеством комментариев). Вывести посты и количество комментариев.
6. Вывести в отдельный csv файл следующую информацию (выводим только те комментарии, в которых есть упоминание о Data Engineering):
    - id поста,
    - дата поста,
    - текст поста,
    - id комментария,
    - дата комментария,
    - текст комментария,
    - автор комментария
