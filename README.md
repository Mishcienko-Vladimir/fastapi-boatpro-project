# ![Логотип BoatPro](docs/icons/logo.png) BoatPro
BoatPro — масштабируемое полнофункциональное e-commerce API-приложение для интернет-магазина водно-моторной техники. 
Позволяет быстро запустить онлайн-платформу с поддержкой товаров, заказов и пользователей. 
Легко адаптируется под другие категории — идеальное решение для стартапа или MVP.

![Изображения стека](docs/images/technology-stack.jpg)

## 📚 Содержание
- [🛠️ Технологический стек](#-технологический-стек)
- [✅ Функционал](#-функционал)
- [📂 Структура проекта](#-структура-проекта)
- [📸 Примеры работы приложения](#-примеры-работы-приложения)
- [📘 Документация API (Swagger UI)](#-документация-api-swagger-ui)
- [🧩 Расширение функционала](#-расширение-функционала)
- [⚙️ Установка и запуск](#-установка-и-запуск)
- [📬 Контакты](#-контакты)

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
  > Комплексная проверка API с помощью `Pytest`: unit-тесты, интеграционные тесты, тесты безопасности и аутентификации. 
  > Поддержка фикстур, моков и покрытия кода через `pytest-cov`.
- **📦 Контейнеризация**  
  > Полная инфраструктура: FastAPI, PostgreSQL, Redis, RabbitMQ, pgAdmin — одной командой.
- **📘 Документация API**  
  > Автогенерация по OpenAPI, доступна по `/docs`.

## 📂 Структура проекта

```bash
fastapi-application/
├── actions                    # Скрипты (создание суперпользователя)
├── alembic                    # Миграции БД 
├── api                        # Всё, что связано с HTTP API
│   ├── api_v1                 # Версия API v1
│   │   ├── dependencies       # Зависимости FastAPI
│   │   ├── routers            # Роутеры, эндпоинты (конечные точки доступа API)
│   │   ├── services           # Бизнес-логика
│   │   └── __init__.py
│   ├── webhooks               # Обработка внешних вебхуков 
│   └── __init__.py            # Регистрация роутеров API и Webhooks
├── core                       # Ядро приложения: модели, схемы, конфигурация
│   ├── dependencies           # Глобальные зависимости (get_db_session, fastapi-users)
│   ├── gunicorn               # Конфигурация Gunicorn
│   ├── models                 # ORM-модели, миксины и помощник для работы с БД
│   ├── repositories           # Операции с БД и файлами
│   ├── schemas                # Pydantic-схемы для валидации данных
│   ├── types                  # Кастомные типы (например, UserId)
│   ├── __init__.py
│   └── config.py              # Настройки приложения через pydantic-settings (.env)
├── mailing                    # Отправка email (подтверждение, сброс пароля и т.д)
├── middleware                 # Кастомные middleware 
├── static                     # Статические файлы
│   ├── css                    # Стили сайта и админ-панели
│   ├── images                 # Изображения товаров и иконки
│   └── js                     # JavaScript для форм, поиска, избранного и т.д.
├── templates                  # HTML-шаблоны (Jinja2)
├── tests                      # Автотесты Pytest (интеграционные и unit тесты)
├── utils                      # Вспомогательные утилиты
│   ├── payment                # Интеграция с YooKassa
│   ├── webhooks               # Вспомогательные функции для вебхуков
│   ├── __init__.py
│   ├── case_converter.py      # Функция конвертации имени таблицы
│   ├── key_builder.py         # Генерация ключей для кэширования в Redis
│   ├── limiter.py             # Инициализация и настройка rate limiting
│   └── templates.py           # Инициализация и настройка Jinja2Templates
├── views                      # View-функции для рендеринга HTML-страниц
├── .env                       # Переменные окружения (не отображается в git)
├── .env.template              # Шаблон .env (автоматически заменяет .env, если его нет)
├── alembic.ini                # Конфигурация Alembic
├── create_fastapi_app.py      # Создания и настройка FastAPI-приложения 
├── errors_handlers.py         # Обработчик ошибок
├── main.py                    # Точка входа: создаёт и запускает приложение
├── prestart.sh                # Скрипт, для запуска миграции перед создания БД в Docker
├── run.py                     # Запуск приложения через Gunicorn (для Docker)
└── run_main.py                # Создания и запуск приложения через Gunicorn
```

## 📸 Примеры работы приложения

<details>
<summary style="font-size: 16px;"><b>🎥 Визуал приложения</b></summary>

https://github.com/user-attachments/assets/3ee276dd-0796-4377-955c-054fa3deaf19
</details>

<details>
<summary style="font-size: 16px;"><b>📝 Регистрация и Аутентификация</b></summary>

https://github.com/user-attachments/assets/ab91299e-f185-4049-ac74-d024592d5ae2
</details>

<details>
<summary style="font-size: 16px;"><b>✅ Подтверждение почты</b></summary>

https://github.com/user-attachments/assets/c9b3eab1-81a6-4675-98b5-1f343416392a
</details>

<details>
<summary style="font-size: 16px;"><b>🔐 Изменения пароля</b></summary>

https://github.com/user-attachments/assets/d252a7aa-ba51-420c-ab2f-235eb2b32fcd
</details>

<details>
<summary style="font-size: 16px;"><b>🗂️ Каталог и страницы с товарами</b></summary>

https://github.com/user-attachments/assets/e9e63dd0-6fc8-4ef7-a398-7940fc6da08c
</details>

<details>
<summary style="font-size: 16px;"><b>📱 Адаптивность страниц</b></summary>

https://github.com/user-attachments/assets/4fe2473d-f650-4c12-8bd5-1bdec112ffe5
</details>

<details>
<summary style="font-size: 16px;"><b>🛒 Покупка товара</b></summary>

https://github.com/user-attachments/assets/823be6f6-1ad6-4709-a048-a2c682a4eb57
</details>

<details>
<summary style="font-size: 16px;"><b>🔍 Поиск товара</b></summary>

https://github.com/user-attachments/assets/6969a831-26a2-4beb-96cf-65125167f21f
</details>

<details>
<summary style="font-size: 16px;"><b>🛠️ Панель администрирования</b></summary>

https://github.com/user-attachments/assets/afb57c40-abb0-4c0a-8a35-9d5406c7d905
</details>

<details>
<summary style="font-size: 16px;"><b>➕ Создание товара</b></summary>

https://github.com/user-attachments/assets/378e47ef-5f4c-4c0b-88cb-ca0528d0dc5c
</details>

<details>
<summary style="font-size: 16px;"><b>🔄 Обновление и удаление товара</b></summary>

https://github.com/user-attachments/assets/581085dc-eedb-4a60-b5b5-0ac4d2b3fbf6
</details>

## 📘 Документация API (Swagger UI)

> BoatPro автоматически генерирует **интерактивную документацию API** по стандарту OpenAPI.
> Документация построена на **Swagger UI** — с возможностью тестирования эндпоинтов прямо в браузере.
> Документация доступна при запущенном приложении по адресу: `http://localhost:8000/docs`

### 🔗 Основные разделы
- `Users 👥` — Управление пользователями
- `Auth 🔐` — Аутентификация и безопасность
- `Boats 🚢` — CRUD катеров
- `Trailers 🚛` — CRUD лодочных прицепов
- `Outboard motors 🔧` — CRUD лодочных моторов
- `Category 📋` - CRUD каталога товаров
- `Favorites 💖` — Работа с избранным
- `Search 🔍` — Поиск товаров
- `Pickup points 📍` — CRUD пунктов самовывоза
- `Orders 🧾` — Управление заказами
- `Webhooks 🔄` — Обработка внешних уведомлений

<details>
<summary><b>🖼️ Изображение эндпоинтов.</b></summary>

![Изображения эндпоинтов](docs/images/swagger.png)
</details>

## 🧩 Расширение функционала

_В данном разделе представлен пример добавления нового раздела `Гидроциклы`._

<details>
<summary><b>1. Добавления модели SQLAlchemy.</b></summary>

> Пометьте главную папку `fastapi-application` как корневой источник.
> > *Нажмите ПКМ по папке `fastapi-application` и выберите `Mark Directory as -> Sources Root`.*
>  
> По пути `core/models/products` создадите новый модуль `jet_ski.py`. И создайте модель гидроциклов.
> ```python
> from sqlalchemy import SmallInteger, ForeignKey, String
> from sqlalchemy.orm import Mapped, mapped_column
> 
> from core.models.products.product_base import Product
> 
>  
> class JetSki(Product):
>     __mapper_args__ = {"polymorphic_identity": "jet_ski"}
> 
>     id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)
>     length_hull: Mapped[int] = mapped_column(SmallInteger, comment="Длина корпуса в см")
>     width_hull: Mapped[int] = mapped_column(SmallInteger, comment="Ширина корпуса в см")
>     weight: Mapped[int] = mapped_column(SmallInteger, comment="Вес в кг")
>     capacity: Mapped[int] = mapped_column(SmallInteger, comment="Количество мест")
>     load_capacity: Mapped[int] = mapped_column(SmallInteger, comment="Грузоподъемность в кг")
>     engine_power: Mapped[int] = mapped_column(SmallInteger, comment="Мощность в л.с.")
>     engine_displacement: Mapped[int] = mapped_column(SmallInteger, comment="Объем в куб.см")
>     fuel_capacity: Mapped[int] = mapped_column(SmallInteger, comment="Топливный бак в л")
>     hull_material: Mapped[str] = mapped_column(String(50), comment="Материал корпуса")
>     gasoline_brand: Mapped[int] = mapped_column(SmallInteger, comment="Марка бензина")
> ```
> Инициализируйте модель `JetSki`. В модуле `core/models/__init__.py` импортируйте модель.
> ```python
> ...
> from .products.jet_ski import JetSki
> ```
</details>

<details>
<summary><b>2. Генерация и применение миграции Alembic.</b></summary>

  > Автоматическая генерация миграции. В терминале выполните команду:
  > ```bash
  >  (.venv) PS ...\BoatPro\fastapi-application> alembic revision --autogenerate -m "Описание миграции"
  > ```
  > Файл с миграции создан в папку `alembic/versions`. Примените миграцию:
  > ```bash
  >  (.venv) PS ...\BoatPro\fastapi-application> alembic upgrade head
  > ```
</details>

<details>
<summary><b>3. Создание Pydantic-схем.</b></summary>

  > Создайте модуль `jet_ski.py` со схемами в папку `core/schemas/products`.
  > ```python
  > from datetime import datetime
  > from typing import Optional
  > from pydantic import Field
  > 
  > from core.schemas.base_model import BaseSchemaModel
  > from .product_base_model import ProductBaseModel
  > from .image_path import ImagePathRead
  > from .category import CategoryRead
  > 
  > 
  > class JetSkiBaseModel(ProductBaseModel):
  >     """Базовая схема для гидроциклов."""
  > 
  >     length_hull: int = Field(gt=0, lt=1000, description="Длина в см")
  >     width_hull: int = Field(gt=0, lt=200, description="Ширина в см")
  >     weight: int = Field(gt=0, lt=1000, description="Вес в кг")
  >     capacity: int = Field(gt=0, lt=10, description="Вместимость")
  >     load_capacity: int = Field(gt=0, lt=1000, description="Грузоподъемность в кг")
  >     engine_power: int = Field(gt=0, lt=1000, description="Мощность двигателя в л.с.")
  >     engine_displacement: int = Field(gt=0, lt=10000, description="Объем двигателя в куб.см")
  >     fuel_capacity: int = Field(gt=0, lt=200, description="Объем топливного бака в л.")
  >     hull_material: str = Field(min_length=1, max_length=50, description="Материал корпуса")
  >     gasoline_brand: int = Field(gt=0, lt=200, description="Марка бензина")
  > 
  > 
  > class JetSkiCreate(JetSkiBaseModel):
  >     """Схема создания."""
  > 
  >     category_id: int = Field(description="ID категории товара")
  > 
  > 
  > class JetSkiUpdate(JetSkiBaseModel):
  >     """Схема частичного обновления."""
  > 
  >     name: Optional[str] = None
  >     price: Optional[int] = None
  >     company_name: Optional[str] = None
  >     description: Optional[str] = None
  >     is_active: Optional[bool] = None
  >     length_hull: Optional[int] = None
  >     width_hull: Optional[int] = None
  >     weight: Optional[int] = None
  >     capacity: Optional[int] = None
  >     load_capacity: Optional[int] = None
  >     engine_power: Optional[int] = None
  >     engine_displacement: Optional[int] = None
  >     fuel_capacity: Optional[int] = None
  >     hull_material: Optional[str] = None
  >     gasoline_brand: Optional[int] = None
  > 
  > 
  > class JetSkiRead(JetSkiBaseModel):
  >     """Схема для чтения."""
  > 
  >     id: int = Field(description="ID гидроцикла")
  >     category: CategoryRead = Field(description="Категория")
  >     created_at: datetime = Field(description="Дата создания")
  >     updated_at: datetime = Field(description="Дата последнего обновления")
  >     images: list[ImagePathRead] = Field(description="Список изображений")
  > 
  > 
  > class JetSkiSummarySchema(BaseSchemaModel):
  >     """Схема с краткой информации."""
  > 
  >     id: int = Field(description="ID гидроцикла")
  >     name: str = Field(min_length=1, max_length=255, description="Название модели")
  >     price: int = Field(gt=0, description="Цена в рублях")
  >     company_name: str = Field(min_length=1, max_length=100, description="Название производителя")
  >     length_hull: int = Field(gt=0, lt=1000, description="Длина в см")
  >     width_hull: int = Field(gt=0, lt=200, description="Ширина в см")
  >     weight: int = Field(gt=0, lt=1000, description="Вес в кг")
  >     capacity: int = Field(gt=0, lt=10, description="Вместимость")
  >     fuel_capacity: int = Field(gt=0, lt=200, description="Объем топливного бака в л.")
  >     engine_power: int = Field(gt=0, lt=1000, description="Мощность двигателя в л.с.")
  >     is_active: bool = Field(description="Наличие товара")
  >     image: Optional[ImagePathRead] = Field(None, description="Главное изображение")
  > ```
</details>

<details>
<summary><b>4. Создание и регистрация эндпоинтво (конечных точек API).</b></summary>

  > Добавьте префикс для кэша и пути роутера jet_skis в core/config.py:
  > ```python
  > ...
  > class ApiV1Prefix(BaseModel):
  >  """Конфигурация префикса API версии 1"""
  >  
  >  jet_skis: str = "/jet-skis"
  > ...
  > 
  > class CacheNamespace(BaseModel):
  >  """Именование пространства кэша"""
  >
  >  jet_skis_list: str = "jet-skis-list"
  >  jet_ski: str = "jet-ski"
  > ...
  > ```
  > Создайте модуль `jet_skis.py` с роутером в папку `api/api_v1/routers/products`. И добавьте эндпоинты с кэшем для гидроциклов:
  > ```python
  > from typing import Annotated
  > from fastapi import APIRouter, Depends, UploadFile, Form, File, status
  > from sqlalchemy.ext.asyncio import AsyncSession
  > 
  > from fastapi_cache import FastAPICache
  > from fastapi_cache.decorator import cache
  > 
  > from api.api_v1.dependencies.create_multipart_form_data import create_multipart_form_data
  > from api.api_v1.services.products import ProductsService
  > 
  > from core.config import settings
  > from core.dependencies import get_db_session
  > from core.models.products.jet_ski import JetSki
  > from core.schemas.products.jet_ski import JetSkiRead, JetSkiUpdate, JetSkiCreate, JetSkiSummarySchema
  > 
  > from utils.key_builder import (
  >     universal_list_key_builder,
  >     get_by_name_key_builder,
  >     get_by_id_key_builder,
  > )
  > 
  > router = APIRouter(prefix=settings.api.v1.jet_skis, tags=["Гидроциклы 🚤"])
  > 
  > @router.post("/", status_code=status.HTTP_201_CREATED, response_model=JetSkiRead)
  > async def create_jet_ski(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_data: Annotated[JetSkiCreate, Depends(create_multipart_form_data(JetSkiCreate))],
  >     images: Annotated[list[UploadFile], File(..., description="Изображения товара")],
  > ) -> JetSkiRead:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     new_jet_ski = await _service.create_product(product_data=jet_ski_data, images=images)
  >     
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_skis_list)
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_ski)
  >     return JetSkiRead.model_validate(new_jet_ski)
  > 
  > @router.get("/jet_ski-name/{jet_ski_name}", status_code=status.HTTP_200_OK, response_model=JetSkiRead)
  > @cache(expire=300, key_builder=get_by_name_key_builder, namespace=settings.cache.namespace.jet_ski)
  > async def get_jet_ski_by_name(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_name: str,
  > ) -> JetSkiRead:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     jet_ski = await _service.get_product_by_name(product_name=jet_ski_name)
  >     return JetSkiRead.model_validate(jet_ski)
  > 
  > @router.get("/jet_ski-id/{jet_ski_id}", status_code=status.HTTP_200_OK, response_model=JetSkiRead)
  > @cache(expire=300, key_builder=get_by_id_key_builder, namespace=settings.cache.namespace.jet_ski)
  > async def get_jet_ski_by_id(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_id: int,
  > ) -> JetSkiRead:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     jet_ski = await _service.get_product_by_id(product_id=jet_ski_id)
  >     return JetSkiRead.model_validate(jet_ski)
  > 
  > @router.get("/", status_code=status.HTTP_200_OK, response_model=list[JetSkiRead])
  > @cache(expire=300, key_builder=universal_list_key_builder, namespace=settings.cache.namespace.jet_skis_list)
  > async def get_jet_skis(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  > ) -> list[JetSkiRead]:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     all_jet_skis = await _service.get_products()
  >     return [JetSkiRead.model_validate(jet_ski) for jet_ski in all_jet_skis]
  > 
  > @router.get("/summary", status_code=status.HTTP_200_OK, response_model=list[JetSkiSummarySchema])
  > @cache(expire=300, key_builder=universal_list_key_builder, namespace=settings.cache.namespace.jet_skis_list)
  > async def get_jet_skis_summary(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  > ) -> list[JetSkiSummarySchema]:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     all_jet_skis = await _service.get_products()
  >     return [JetSkiSummarySchema.model_validate(
  >             {
  >                 **jet_ski.__dict__,
  >                 "image": jet_ski.images[0] if jet_ski.images else None,
  >             }
  >         ) for jet_ski in all_jet_skis
  >     ]
  > 
  > @router.patch("/{jet_ski_id}", status_code=status.HTTP_200_OK, response_model=JetSkiRead)
  > async def update_jet_ski_data_by_id(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_id: int,
  >     jet_ski_data: JetSkiUpdate,
  > ) -> JetSkiRead:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     jet_ski = await _service.update_product_data_by_id(
  >         product_id=jet_ski_id,
  >         product_data=jet_ski_data,
  >     )
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_skis_list)
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_ski)
  >     return JetSkiRead.model_validate(jet_ski)
  > 
  > @router.patch("/images/{jet_ski_id}", status_code=status.HTTP_200_OK, response_model=JetSkiRead)
  > async def update_jet_ski_images_by_id(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_id: int,
  >     remove_images: str | None = Form(None, description="id изображений для удаления, через запятую, без пробелов"),
  >     add_images: list[UploadFile] = File(..., description="Новые изображения для товара"),
  > ) -> JetSkiRead:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     jet_ski = await _service.update_product_images_by_id(
  >         product_id=jet_ski_id,
  >         remove_images=remove_images,
  >         add_images=add_images,
  >     )
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_skis_list)
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_ski)
  >     return JetSkiRead.model_validate(jet_ski)
  > 
  > @router.delete("/{jet_ski_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
  > async def delete_jet_ski_by_id(
  >     session: Annotated[AsyncSession, Depends(get_db_session)],
  >     jet_ski_id: int,
  > ) -> None:
  >     _service = ProductsService(session=session, product_db=JetSki)
  >     delete_jet_ski = await _service.delete_product_by_id(product_id=jet_ski_id)
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_skis_list)
  >     await FastAPICache.clear(namespace=settings.cache.namespace.jet_ski)
  >     return delete_jet_ski
  > ```
  > Инициализируйте роутер гидроциклов. В инициализатор `api/api_v1/routers/products/__init__.py`, добавьте:
  > ```python
  > ...
  > from .jet_skis import router as jet_skis_router
  > 
  > router = APIRouter(prefix=settings.api.v1.products)
  > 
  > router.include_router(jet_skis_router)
  > ...
  > ```
  > Получаем полностью функциональный API-раздел для управления гидроциклами. 
  > Доступный в интерактивной документации Swagger UI по адресу `http://localhost:8000/docs`.

![Изображения эндпоинтов гидроциклов](docs/images/jet-skis-docs.png)

**Все эндпоинты:**
- ✅ Автоматически задокументированы
- ✅ Поддерживают кэширование через Redis
- ✅ Обеспечивают валидацию входных данных (Pydantic)
- ✅ Интегрированы с общей бизнес-логикой через `ProductsService`
- ✅ Участвуют в общей системе очистки кэша при изменениях
</details>

<details>
<summary><b>5. Расширение `views` и шаблонов: добавление HTML-страниц для гидроциклов.</b></summary>

- 🖼️ **Создания шаблонов HTML-страниц** — [см. `frontend-templates.md`](docs/guides/frontend-templates.md)  
- 🧩 **Создания View-функции** — [см. `frontend-views.md`](docs/guides/frontend-views.md)

**✅ Что теперь доступно:**
- 📄 **Каталог гидроциклов** — список с краткими характеристиками
- 🔍 **Детальная страница товара** — полное описание, галерея, управление "В избранное" и "Купить"
- 🛠️ **Админ-панель** — полный CRUD через веб-интерфейс

> После реализации API для гидроциклов, добавлены **HTML-представления** для пользователей и администраторов, построенные 
> на **Jinja2-шаблонах** и интегрированные с существующей системой роутинга.

![Изображения гидроциклов](docs/images/new-category.png)
</details>

_Архитектура остаётся **масштабируемой**: добавление новых категорий (например, ПВХ лодки или яхты) требует аналогичных шагов._

## ⚙️ Установка и запуск

1. **Клонируйте репозиторий**
> В терминале выполните команду:
> ```bash
> git clone https://github.com/Mishchenko-Vladimir/fastapi-boatpro-project.git
> ```
> Перейдите в директорию проекта:
> ```bash
> cd fastapi-boatpro-project
> ```

2. **Настройка переменных окружения**
> Заполните файлы `.env.template` и `docker-compose.yml` своими значениями.
 
3. **Запустите приложение через Docker**
> Сборка образа с именем `app`:
> ```bash
> docker compose build app
> ```
> Запуск сборки (приложения):
> ```bash
> docker compose up -d
> ```
> Остальные команды `docker`:
> - `docker compose ps` - посмотреть какие контейнеры запущены
> - `docker compose logs` -f app - посмотреть логи приложения
> - `docker compose stop` - остановка приложения
> - `docker compose down` - удаления сборки

## 📬 Контакты

### 💻 Автор: Мищенко Владимир
- **GitHub:** [Mishchenko-Vladimir](https://github.com/Mishchenko-Vladimir)
- **Mail.ru:** [mishchienko.2001@mail.ru](mailto:mishchienko.2001@mail.ru)
- **Gmail:** [mishchieko.2001@gmail.com](mailto:mishchieko.2001@gmail.com)
- **Telegram:** [@VM_Dev](https://t.me/VM_Dev)

💌 Не забудьте поставить звезду ⭐ на GitHub, если вам понравился проект! 😉

---
[↑ Вернуться наверх](#-boatpro)
