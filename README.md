# ![Логотип BoatPro](docs/icons/logo.png) BoatPro
BoatPro — масштабируемое полнофункциональное e-commerce API-приложение для интернет-магазина водно-моторной техники. Позволяет быстро запустить онлайн-платформу с поддержкой товаров, заказов и пользователей. Легко адаптируется под другие категории — идеальное решение для стартапа или MVP.

![Изображения стека](docs/images/technology-stack.jpg)

## 🛠️ Технологический стек

| Компоненты | |
|----------|---:|
| **🐍 Язык:** Python 3.12+ | [![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) |
| **⚡ Фреймворк:** FastAPI | [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/) |
| **🌐 Фронтенд:** HTML + CSS + JavaScript | [![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/ru/docs/Web/HTML) [![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/ru/docs/Web/CSS) [![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/ru/docs/Web/JavaScript) |
| **🚀 ASGI-сервер:** Uvicorn + Gunicorn | [![Uvicorn](https://img.shields.io/badge/Uvicorn-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://www.uvicorn.org/) [![Gunicorn](https://img.shields.io/badge/Gunicorn-F46D43?style=for-the-badge&logo=apache&logoColor=white)](https://gunicorn.org/) |
| **🗄️ База Данных:** PostgreSQL + asyncpg | [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/) [![asyncpg](https://img.shields.io/badge/asyncpg-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://magicstack.github.io/asyncpg/) |
| **🔁 ORM:** SQLAlchemy (async) | [![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://www.sqlalchemy.org/) |
| **🔄 Миграции БД:** Alembic | [![Alembic](https://img.shields.io/badge/Alembic-0B5566?style=for-the-badge&logo=python&logoColor=white)](https://alembic.sqlalchemy.org/) |
| **🔐 Аутентификация:** FastAPI-Users | [![FastAPI-Users](https://img.shields.io/badge/FastAPI--Users-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi-users.github.io/fastapi-users/) |
| **✅ Валидация:** Pydantic v2 + pydantic-settings | [![Pydantic](https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/) [![pydantic--settings](https://img.shields.io/badge/pydantic--settings-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| **🧩 Кэширование:** Redis | [![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/) |
| **📨 Очереди:** RabbitMQ (Pika) | [![RabbitMQ](https://img.shields.io/badge/RabbitMQ-F16737?style=for-the-badge&logo=rabbitmq&logoColor=white)](https://www.rabbitmq.com/) [![Pika](https://img.shields.io/badge/Pika-F16737?style=for-the-badge&logo=python&logoColor=white)](https://pika.readthedocs.io/) |
| **📄 Шаблонизация:** Jinja2 | [![Jinja2](https://img.shields.io/badge/Jinja2-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://jinja.palletsprojects.com/) |
| **📝 Логирование:** logging | [![Logging](https://img.shields.io/badge/Logging-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/logging.html) |
| **🛡️ Защита:** slowapi + CORS | [![slowapi](https://img.shields.io/badge/slowapi-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://slowapi.readthedocs.io/) [![CORS](https://img.shields.io/badge/CORS-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://fastapi.tiangolo.com/tutorial/cors/) |
| **💳 Оплата:** YooKassa | [![YooKassa](https://img.shields.io/badge/YooKassa-1E90FF?style=for-the-badge&logo=yandex&logoColor=white)](https://yookassa.ru/) |
| **📧 Почта:** aiosmtplib | [![aiosmtplib](https://img.shields.io/badge/aiosmtplib-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://aiosmtplib.readthedocs.io/) |
| **📁 Загрузка файлов:** aiofiles + python-multipart | [![aiofiles](https://img.shields.io/badge/aiofiles-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://github.com/Tinche/aiofiles) [![python--multipart](https://img.shields.io/badge/python--multipart-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://andrew-d.github.io/python-multipart/) |
| **📦 Зависимости:** Poetry | [![Poetry](https://img.shields.io/badge/Poetry-6D3BA9?style=for-the-badge&logo=python&logoColor=white)](https://python-poetry.org/) |
| **🐳 Контейнеризация:** Docker + Docker Compose | [![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/) [![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/) |
| **🧪 Тестирование:** Pytest + httpx + faker | [![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/) [![HTTPX](https://img.shields.io/badge/HTTPX-0A9EDC?style=for-the-badge&logo=python&logoColor=white)](https://www.python-httpx.org/) [![Faker](https://img.shields.io/badge/Faker-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://faker.readthedocs.io/) |
| **📘 Документация:** OpenAPI (Swagger UI) | [![OpenAPI](https://img.shields.io/badge/OpenAPI-10985B?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io/specification/) |

## ✅ Функционал

- **🔐 Аутентификация и безопасность**  
  > Регистрация, вход, подтверждение email, восстановление пароля.  
  > Ограничение частоты запросов (`rate limiting`) для защиты от bruteforce.  
  > `CORS` с настройкой доверенных доменов.  
  > Асинхронная отправка писем: подтверждение, сброс пароля, уведомления.
- **🛠️ Панель администратора**  
  > Полный `CRUD` для моделей: товары, категории, заказы, пользователи, пункты выдачи.
- **🗂️ Каталог товаров**  
  > Разделён на категории: лодки, подвесные моторы, прицепы.  
  > Каждый товар — с описанием, характеристиками и фото.
- **📄 Детальные страницы товаров**  
  > Полное описание, галерея изображений, кнопки `"В избранное"` и `"Купить"`.
- **🔍 Поиск товаров**  
  > Поиск по названию, бренду или описанию с поддержкой частичного совпадения.
- **🧾 Оформление заказов**  
  > Добавление товаров, выбор пункта самовывоза, оплата через `YooKassa`.  
  > Статусы: "Ожидает оплаты", "Оплачен", "Готов к выдаче", "Завершён".
- **❤️ Добавление товаров в избранное**  
  > Пользователи могут добавлять товары в избранное.
- **🔄 Миграции и суперпользователя**  
  > Автоматическое применение миграций Alembic и создание суперпользователя при старте.
- **🧩 Кэширование и фоновые задачи**  
  > Ускорение API через `Redis`. Асинхронная обработка (отправка писем).
- **📝 Логирование**  
  > Полная система логирования всех ключевых операций: аутентификация, заказы, ошибки, запросы. Готово к интеграции с ELK/Sentry.
- **🧪 Тестирование**  
  > Комплексная проверка API с помощью `Pytest`: unit-тесты, интеграционные тесты, тесты безопасности и аутентификации. Поддержка фикстур, моков и покрытия кода через `pytest-cov`.
- **📦 Контейнеризация**  
  > Полная инфраструктура: FastAPI, PostgreSQL, Redis, RabbitMQ, pgAdmin — одной командой.
- **📘 Документация API**  
  > Автогенерация по OpenAPI, доступна по `/docs`.
