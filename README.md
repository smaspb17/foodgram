Домен - food-gramm.ru

Логин - admin

Пароль - allpip17 

# Foodgram

![Actions Status](https://github.com/smaspb17/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## ОПИСАНИЕ:

Foodgram - это учебный веб-сайт для оттачивания разработки бэкэнда, на котором пользователи публикуют кулинарные рецепты с картинками, добавлять чужие рецепты в избранное, подписываются на публикации других авторов. Пользователям сайта будет доступен сервис «Список покупок», который позволяет создавать и скачивать список продуктов, которые необходимо купить для приготовления выбранных блюд.

Бэкэнд проекта разрабатан с использованием Django REST framework с реализацией REST API, включает в себя компоненты, необходимые для предоставления API-сервисов, такие как маршрутизация URL, сериализаторы, модели, представления, аутентификация djoser, управление доступом, фильтрация, пагинация, валидация данных. DRF обеспечивает поддержку формата зaпросов JSON. 

Фронтенд — одностраничное SPA-приложение, написанное на фреймворке React.

База данных - PostgreSQL.

## СТЕК ТЕХНОЛОГИЙ БЭКЭНДА:
Python 3.9.10, Django Rest Framework 3.14.0, PostgreSQL, djoser, JWT, Pillow, JSON, Telegram, YAML, docker-compose, Gunicorn, Nginx, CI/CD, Postman

## УСТАНОВКА ПРОЕКТА на боевой сервер

Клонируй репозиторий на ПК и перейди в него в командной строке:

``` 
git clone git@github.com:smaspb17/foodgram-project-react.git
``` 
``` 
cd foodgram-project-react/infra/
``` 
Установи на сервер docker и docker-compose.
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```
Создай на сервере директорию foodgram/infra/:

```
mkdir foodgram/infra/
```
Скопируй в созданную на сервере директорию файлы docker-compose.production.yml и nginx.conf. В случае необходимости введи пароль доступа к северу:
```
scp -i <path_to_SSH/SSH_name> docker-compose.production.yml <username>@<server_ip>:/home/<username>/foodgram/infra/docker-compose.production.yml
scp -i <path_to_SSH/SSH_name> nginx.conf <username>@<server_ip>:/home/<username>/foodgram/infra/nginx.conf

```
Добавь в Secrets на Github следующие переменные:
```
DEBUG=False # режим продакшена
SECRET_KEY=... # секретный ключ Django
ALLOWED_HOSTS=127.0.0.1 localhost <IP адрес/имя домена где разворачиваешь проект>
POSTGRES_DB=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД
DB_HOST=db # название сервиса БД (контейнера) 
DB_PORT=5432 # порт для подключения к БД
DOCKER_PASSWORD=... # Пароль от аккаунта на DockerHub
DOCKER_USERNAME=... # Username в аккаунте на DockerHub
HOST=... # IP удалённого сервера
USER=... # Логин на удалённом сервере
SSH_KEY=... # SSH-key компьютера, с которого будет происходить подключение к удалённому серверу
SSH_PASSPHRASE=... #Если для ssh используется фраза-пароль
TELEGRAM_TO=... #ID пользователя в Telegram
TELEGRAM_TOKEN=... #ID бота в Telegram
```

Выполни локально в терминале команды:
```
git add .
git commit -m "Коммит"
git push
```

На GitHub создай и закрой Pull request c ветки develop в ветку main.

После этого будут запущены процессы workflow:

*   проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8)
*   сборка и доставка докер-образов для контейнеров backend и frontend на Docker Hub
*   автоматический деплой проекта на боевой сервер
*   отправка уведомления в Telegram о том, что процесс деплоя успешно завершился

На сервере выполни команды миграции и сбор статики:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input 
```

Создай суперюзера и загрузи в базу данных информацию об ингредиентах:
```
sudo docker exec -it <backend_container_name/ID> python manage.py createsuperuser
```
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py database_load
```
## Запуск проекта локально:

Клонируй репозиторий на ПК и перейди в него в командной строке:
``` 
git clone git@github.com:smaspb17/foodgram-project-react.git
``` 
``` 
cd foodgram-project-react/backend/
``` 
Создай и активируй виртуальное окружение:

```
python -m venv venv
``` 
* Если у вас Linux/macOS:
```
source venv/bin/activate
``` 

* Если у вас Windows:
``` 
source venv/Scripts/activate
```

Обнови пакет pip
```
python.exe -m pip install --upgrade pip
``` 

Установи зависимости из файла requirements:

```
pip install -r requirements.txt
``` 

Выполнить миграции:
```
python manage.py makemigrations
``` 
```
python manage.py migrate
``` 
Загрузи в базу данных информацию об ингредиентах:
```
python manage.py database_load
```

Запустить проект:

```
python manage.py runserver
``` 

## В API доступны следующие эндпоинты:

* ```/api/users/```  Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя. Доступно без токена.

* ```/api/users/{id}``` GET-запрос – персональная страница пользователя с указанным id (доступно без токена).

* ```/api/users/me/``` GET-запрос – страница текущего пользователя. PATCH-запрос – редактирование собственной страницы. Доступно авторизированным пользователям. 

* ```/api/users/set_password``` POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям. 

* ```/api/auth/token/login/``` POST-запрос – получение токена. Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.

* ```/api/auth/token/logout/``` POST-запрос – удаление токена. 

* ```/api/tags/``` GET-запрос — получение списка всех тегов. Доступно без токена.

* ```/api/tags/{id}``` GET-запрос — получение информации о теге о его id. Доступно без токена. 

* ```/api/ingredients/``` GET-запрос – получение списка всех ингредиентов. Подключён поиск по частичному вхождению в начале названия ингредиента. Доступно без токена. 

* ```/api/ingredients/{id}/``` GET-запрос — получение информации об ингредиенте по его id. Доступно без токена. 

* ```/api/recipes/``` GET-запрос – получение списка всех рецептов. Возможен поиск рецептов по тегам и по id автора (доступно без токена). POST-запрос – добавление нового рецепта (доступно для авторизированных пользователей).

* ```/api/recipes/?is_favorited=1``` GET-запрос – получение списка всех рецептов, добавленных в избранное. Доступно для авторизированных пользователей. 

* ```/api/recipes/is_in_shopping_cart=1``` GET-запрос – получение списка всех рецептов, добавленных в список покупок. Доступно для авторизированных пользователей. 

* ```/api/recipes/{id}/``` GET-запрос – получение информации о рецепте по его id (доступно без токена). PATCH-запрос – изменение собственного рецепта (доступно для автора рецепта). DELETE-запрос – удаление собственного рецепта (доступно для автора рецепта).

* ```/api/recipes/{id}/favorite/``` POST-запрос – добавление нового рецепта в избранное. DELETE-запрос – удаление рецепта из избранного. Доступно для авторизированных пользователей. 

* ```/api/recipes/{id}/shopping_cart/``` POST-запрос – добавление нового рецепта в список покупок. DELETE-запрос – удаление рецепта из списка покупок. Доступно для авторизированных пользователей. 

* ```/api/recipes/download_shopping_cart/``` GET-запрос – получение текстового файла со списком покупок. Доступно для авторизированных пользователей. 

* ```/api/users/{id}/subscribe/``` GET-запрос – подписка на пользователя с указанным id. POST-запрос – отписка от пользователя с указанным id. Доступно для авторизированных пользователей

* ```/api/users/subscriptions/``` GET-запрос – получение списка всех пользователей, на которых подписан текущий пользователь Доступно для авторизированных пользователей. 

## АВТОР:

Шайбаков Марат

## ЛИЦЕНЗИЯ:

нет

## КОНТАКТЫ:

smaspb17@yandex.ru
