<style>
.tech-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  margin-left: 10px;
}
.tech-row a {
  flex-shrink: 0;
}
.tech-row a:hover img {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}
</style>


# ![Логотип BoatPro](docs/icons/logo.png) BoatPro
BoatPro — масштабируемое полнофункциональное e-commerce API-приложение для интернет-магазина водно-моторной техники. Позволяет быстро запустить онлайн-платформу с поддержкой товаров, заказов и пользователей. Легко адаптируется под другие категории — идеальное решение для стартапа или MVP.

---
## 🛠️ Технологический стек

<div class="tech-row">
  <div>
    <strong>🐍 Язык:</strong> Python 3.12+
  </div>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>⚡ Фреймворк:</strong> FastAPI
  </div>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>🌐 Фронтенд:</strong> HTML + CSS + JavaScript (Vanilla)
  </div>
  <div>
    <a href="https://developer.mozilla.org/ru/docs/Web/HTML">
      <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
    </a>
    <a href="https://developer.mozilla.org/ru/docs/Web/CSS">
      <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS">
    </a>
    <a href="https://developer.mozilla.org/ru/docs/Web/JavaScript">
      <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>🚀 ASGI-сервер:</strong> Uvicorn + Gunicorn
  </div>
  <div>
    <a href="https://www.uvicorn.org/">
      <img src="https://img.shields.io/badge/Uvicorn-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="Uvicorn">
    </a>
    <a href="https://gunicorn.org/">
      <img src="https://img.shields.io/badge/Gunicorn-F46D43?style=for-the-badge&logo=apache&logoColor=white" alt="Gunicorn">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>🗄️ База Данных:</strong> PostgreSQL + asyncpg
  </div>
  <div>
    <a href="https://www.postgresql.org/">
      <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
    </a>
    <a href="https://magicstack.github.io/asyncpg/">
      <img src="https://img.shields.io/badge/asyncpg-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="asyncpg">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>🔁 ORM:</strong> SQLAlchemy (async)
  </div>
  <a href="https://www.sqlalchemy.org/">
    <img src="https://img.shields.io/badge/SQLAlchemy-0B5566?style=for-the-badge&logo=python&logoColor=white" alt="SQLAlchemy">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>🔄 Миграции БД:</strong> Alembic
  </div>
  <a href="https://alembic.sqlalchemy.org/">
    <img src="https://img.shields.io/badge/Alembic-0B5566?style=for-the-badge&logo=python&logoColor=white" alt="Alembic">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>🔐 Аутентификация:</strong> FastAPI-Users
  </div>
  <a href="https://fastapi-users.github.io/fastapi-users/">
    <img src="https://img.shields.io/badge/FastAPI--Users-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI-Users">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>✅ Валидация:</strong> Pydantic v2 + pydantic-settings
  </div>
  <div>
    <a href="https://docs.pydantic.dev/">
      <img src="https://img.shields.io/badge/Pydantic-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Pydantic v2">
    </a>
    <a href="https://docs.pydantic.dev/latest/concepts/pydantic_settings/">
      <img src="https://img.shields.io/badge/pydantic--settings-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="pydantic-settings">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>🧩 Кэширование:</strong> Redis
  </div>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>📨 Очереди:</strong> RabbitMQ (Pika)
  </div>
  <div>
    <a href="https://www.rabbitmq.com/">
      <img src="https://img.shields.io/badge/RabbitMQ-F16737?style=for-the-badge&logo=rabbitmq&logoColor=white" alt="RabbitMQ">
    </a>
    <a href="https://pika.readthedocs.io/">
      <img src="https://img.shields.io/badge/Pika-F16737?style=for-the-badge&logo=python&logoColor=white" alt="Pika">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>📄 Шаблонизация:</strong> Jinja2
  </div>
  <a href="https://jinja.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Jinja2-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Jinja2">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>📝 Логирование:</strong> logging
  </div>
  <a href="https://docs.python.org/3/library/logging.html">
    <img src="https://img.shields.io/badge/Logging-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="logging">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>🛡️ Защита:</strong> slowapi + кастомный CORS
  </div>
  <div>
    <a href="https://slowapi.readthedocs.io/">
      <img src="https://img.shields.io/badge/slowapi-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="slowapi">
    </a>
    <a href="https://fastapi.tiangolo.com/tutorial/cors/">
      <img src="https://img.shields.io/badge/CORS-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="CORS">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>💳 Оплата:</strong> YooKassa
  </div>
  <a href="https://yookassa.ru/">
    <img src="https://img.shields.io/badge/YooKassa-1E90FF?style=for-the-badge&logo=yandex&logoColor=white" alt="YooKassa">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>📧 Почта:</strong> aiosmtplib
  </div>
  <a href="https://aiosmtplib.readthedocs.io/">
    <img src="https://img.shields.io/badge/aiosmtplib-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="aiosmtplib">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>📁 Загрузка файлов:</strong> aiofiles + python-multipart
  </div>
  <div>
    <a href="https://github.com/Tinche/aiofiles">
      <img src="https://img.shields.io/badge/aiofiles-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="aiofiles">
    </a>
    <a href="https://andrew-d.github.io/python-multipart/">
      <img src="https://img.shields.io/badge/python--multipart-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="python-multipart">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>📦 Управление зависимостями:</strong> Poetry
  </div>
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/Poetry-6D3BA9?style=for-the-badge&logo=python&logoColor=white" alt="Poetry">
  </a>
</div>

<div class="tech-row">
  <div>
    <strong>🐳 Контейнеризация:</strong> Docker + Docker Compose
  </div>
  <div>
    <a href="https://www.docker.com/">
      <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    </a>
    <a href="https://docs.docker.com/compose/">
      <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>🧪 Тестирование:</strong> Pytest + httpx + faker
  </div>
  <div>
    <a href="https://docs.pytest.org/">
      <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest">
    </a>
    <a href="https://www.python-httpx.org/">
      <img src="https://img.shields.io/badge/HTTPX-0A9EDC?style=for-the-badge&logo=python&logoColor=white" alt="httpx">
    </a>
    <a href="https://faker.readthedocs.io/">
      <img src="https://img.shields.io/badge/Faker-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="faker">
    </a>
  </div>
</div>

<div class="tech-row">
  <div>
    <strong>📘 Документация:</strong> OpenAPI (автоматически через Swagger UI)
  </div>
  <a href="https://swagger.io/specification/">
    <img src="https://img.shields.io/badge/OpenAPI-10985B?style=for-the-badge&logo=swagger&logoColor=white" alt="OpenAPI">
  </a>
</div>


---

в котором реализована:
- Система пользователей: регистрация, аутентификация, подтверждение email и восстановление пароля через FastAPI-Users.
- Панель администрирования. В которой добавлена возможность: добавлять, изменять, а также удалаять интерисующие модели.
- Страницы с каталогом товаров: лодки, подвесные моторы и прицепы — с детальной информацией, характеристиками и изображениями.
- Поиск товара по названию, имени компании или описанию.
- Избранное: пользователи могут добавлять товары в избранное для быстрого доступа.
- Заказы: добавление товаров, выбор пункта самовывоза и формирование заказа. Оплата заказа с помощью yookassa. Отслеживания статуса заказа.
- Управление изображениями: загрузка, хранение и ассоциация изображений с товарами.
- Миграции базы данных: автоматическое применение изменений структуры БД через Alembic при старте приложения.
- Кэширование и фоновые задачи: поддержка Redis для ускорения работы и асинхронной обработки (например, отправки писем).
- Адаптивная конфигурация: гибкие настройки через pydantic-settings, включая параметры БД, логирования и Gunicorn.
- Документация API: автоматически генерируемый Swagger UI доступен по адресу /docs.
- Контейнеризация: полная инфраструктура на Docker и Docker Compose, включая PostgreSQL, Redis и pgAdmin для удобного управления.