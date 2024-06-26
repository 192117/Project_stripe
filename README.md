# Простой сервер с одной html страничкой, который общается со Stripe и создает платёжные формы для товаров.

## Описание работы сервера:

_Валюты реализованные на сервере доллары (USD) и евро (EUR). Количество в заказах всегда 1 шт (так как реализации изменяемого
количества в заказе не стояло)._

* `cancel/`
Страница отмены платежа или в случае неудачи.
* `success/`
Страница совершения успешного платежа
* `buy/int:id/str:currency/`
Принимает GET запрос с id Item, возвращает session_id с помощью библиотеки stripe.
* `item/int:id/`
Принимает GET запрос с id Item, возвращает простую HTML страницу с двумя кнопками купить в долларах и в  евро. По нажатию
на кнопки происходит запрос на `buy/int:id/str:currency/` , где получается session_id и далее с помощью JS библиотеки 
Stripe происходит редирект на Chekout форму Stripe.
* `buy_cart/int:id/str:currency/`
* Принимает GET запрос с id Order, возвращает session_id с помощью библиотеки stripe.
* `cart/int:id/`
* Принимает GET запрос с id Order, возвращает простую HTML страницу с двумя кнопками купить в долларах и в  евро. По нажатию
на кнопки происходит запрос на `buy_cart/int:id/str:currency/` , где получается session_id и далее с помощью JS библиотеки 
Stripe происходит редирект на Chekout форму Stripe.

Используются также скидка/купоны (Discount) и налог (Tax) для корзин с товарами. Скидка вычитается из общей суммы корзины,
а налог отображается, как уже включенный в цену.

## Реализация сервера:

Пакетным менеджером в проекте является **Poetry**. \
База данных используется **PostgreSQL**. \
Переменные окружения находятся в файле .env.docker, которые затем подгружаются в настройки с помощью **python-dotenv**. Для 
примера смотрите файл .env_example


## Разворачивание сервера:

_Для быстрого разворачивания сервера используется Docker._

1. Для запуска сервера создайте файл **_.env.docker_** рядом с файлом **_.env_example_** и аналогичный ему.
2. Запустите команду _**`docker-compose up -d`**_.
3. Зайдите в контейнер с web командой `docker exec -it CONTAINER_ID /bin/bash`
4. Создайте суперпользователя командой `python stripe_project/manage.py createsuperuser`
5. Перейдите в админку по адресу http://localhost:8000/admin/
6. Создайте товары, корзину, скидки и налог.
7. Можете начинать обращаться по соответствующим url'ам.


## Доступ к серверу:

http://157.90.14.181:8000/admin/ - для создания товаров, корзин, скидок и налога.

Для доступа можете использовать тестовые данные: логин - test_admin, пароль - 123456789admin

- [Отмена/Неудача]()
- [Успешно]()
- [Товар]()
- [Корзина]()
