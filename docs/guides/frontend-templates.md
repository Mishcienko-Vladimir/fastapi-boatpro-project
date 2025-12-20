## Создание HTML-страниц

Добавим изображения гидроцикла в папку `/static/images/website/categories/`.
Дополним HTML-страницу `catalog` в `templates/products`.
```html
...
<div class="category"
  <a href="{{ url_for('jet_skis') }}" title="Гидроциклы">
    <img src="/static/images/website/categories/jet-ski.jpg" alt="Гидроциклы">
    <div class="category-title">Гидроциклы</div>
  </a>
</div>
...
```
Создадим в этой папке страницу `jet-skis.html`.
```html
{% extends "base.html" %}
{% block title %}
  Гидроциклы
{% endblock %}

{% block main %}
  <h1>Гидроциклы</h1>
  <div class="bloc-products">
    {% for jet_ski in jet_skis_list %}
      <div class="product">
        <a href="{{ url_for('jet_ski_detail', jet_ski_name=jet_ski.name|replace(' ', '%20')) }}"
          title="Гидроцикл"
          class="product-link"
          data-product-id="{{ jet_ski.id }}">
          <img class="product-img" src="{{ jet_ski.image.path }}" alt="Гидроцикл">
        </a>
        <div class="product-desc">
          <div class="product-title">{{ jet_ski.name }}</div>
          <div class="product-price">Цена: {{ jet_ski.price }} ₽</div>
          <ul>
            <li>
              <span title="Длинна корпуса">
                <ion-icon name="swap-vertical" alt="Длинна корпуса" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.length_hull }} см
            </li>
            <li>
              <span title="Ширина корпуса">
                <ion-icon name="swap-horizontal" alt="Ширина корпуса" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.width_hull }} см
            </li>
            <li>
              <span title="Вес гидроцикла">
                <ion-icon name="barbell" alt="Вес гидроцикла" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.weight }} кг
            </li>
            <li>
              <span title="Вместимость">
                <ion-icon name="man" alt="Вместимость" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.capacity }} чел
            </li>
            <li>
              <span title="Объем топливного бака">
                <ion-icon name="water" alt="Объем топливного бака" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.fuel_capacity }} л
            </li>
            <li>
              <span title="Мощность двигателя">
                <ion-icon name="flash" alt="Мощность двигателя" style="pointer-events: none;"></ion-icon>
              </span>
              &nbsp;{{ jet_ski.engine_power }} л.с.
            </li>
          </ul>
        </div>
      </div>
    {% endfor %}
  </div>
{% endblock %}
```
Также создадим `jet-ski-detail.html`, шаблон страницы с детальной информации о каждом гидроцикле.
```html
{% extends "base.html" %}
{% block title %}
  {{ jet_ski.name }}
{% endblock %}

 {% block main %}
<div class="basic-bloc">
    <h1>{{ jet_ski.name }}</h1>

    <div class="bloc-product-images">
      <div class="main-image">
        <img id="main-img" src="{{ jet_ski.images[0].path }}" alt="Главное изображение гидроцикла">
        <div class="image-navigation">
          <button class="nav-button prev">&#10094;</button>
          <button class="nav-button next">&#10095;</button>
        </div>
      </div>
      <div class="thumbnails">
        {% for image in jet_ski.images %}
          <img
          src="{{ image.path }}"
          alt="Миниатюра"
          class="{% if loop.first %} active {% endif %}">
        {% endfor %}
       </div>
    </div>

    <div class="bloc-price-info">
      {% if jet_ski.is_active %}
        <span class="status-available">В наличии</span>
      {% else %}
        <span class="status-unavailable">Нет в наличии</span>
      {% endif %}
      <p>Цена: {{ jet_ski.price }} ₽</p>
      <button id="btnBuy" class="btn-buy">Купить</button>
      <button id="btnAddFavorites" class="btn-favorites">В избранное</button>
    </div>

    <div class="bloc-product-info">
      <ul class="product-nav-tabs">
        <li class="nav-item">
          <a class="nav-link active" data-tab="description">Описание</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-tab="features">Характеристики</a>
        </li>
      </ul>
      <div class="tab-content">
        <div id="description" class="tab-pane active">
          <p>{{ jet_ski.description or 'Нет описания' }}</p>
        </div>
        <div id="features" class="tab-pane">
          <table>
            <tr>
              <td class="td-label">Производитель</td>
              <td class="td-value"> {{ jet_ski.company_name }}</td>
            </tr>
            <tr>
              <td class="td-label">Длина корпуса</td>
              <td class="td-value"> {{ jet_ski.length_hull }} см</td>
            </tr>
            <tr>
              <td class="td-label">Вместимость</td>
              <td class="td-value"> {{ jet_ski.capacity }} чел</td>
            </tr>
            <tr>
              <td class="td-label">Грузоподъемность</td>
              <td class="td-value"> {{ jet_ski.load_capacity }} кг</td>
            </tr>
            <tr>
              <td class="td-label">Мощность двигателя</td>
              <td class="td-value"> {{ jet_ski.engine_power }} л.с.</td>
            </tr>
            <tr>
              <td class="td-label">Объем двигателя</td>
              <td class="td-value"> {{ jet_ski.engine_displacement}} куб.см</td>
            </tr>
            <tr>
              <td class="td-label">Объем топливного бака</td>
              <td class="td-value"> {{ jet_ski.fuel_capacity}} л</td>
            </tr>
            <tr>
              <td class="td-label">Материал корпуса</td>
              <td class="td-value"> {{ jet_ski.hull_material }}</td>
            </tr>
            <tr>
              <td class="td-label">Марка бензина</td>
              <td class="td-value"> {{ jet_ski.gasoline_brand}}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>

  <input type="hidden" id="user-id" value="{{ user.id }}">
  <input type="hidden" id="product-id" value="{{ jet_ski.id }}">

  <script src="/static/js/order.js"></script>
{% endblock %}
```
Расширим Admin-panel. Добавим ссылку в `templates/admin/admin-base.html` на новую страницу с администрированием гидроциклов:
```html
...
<a href="{{ url_for('admin_jet_skis') }}">
  <ion-icon name="boat-outline" alt="Гидроциклы"></ion-icon>
  &nbsp; Гидроциклы
</a>
...
```
Создадим новую страницу администрирования гидроциклов `templates/admin/jet-skis.html`:
```html
{% extends "admin/admin-base.html" %}
{% block title %}
  Admin Panel - Гидроциклы
{% endblock %}

{% block main %}
  <h2>Панель управления гидроциклами</h2>
  <div class="window_content">
    {% for jet_ski in jet_skis_list %}
      <div class="data_content">
        <h3>{{ jet_ski.name }}</h3>
        <p><strong>ID товара:</strong> {{ jet_ski.id }}</p>
        <p><strong>Производитель:</strong> {{ jet_ski.company_name }}</p>
        <p><strong>Наличие:</strong> {{ 'В наличие' if jet_ski.is_active else 'Нет в наличие' }}</p>
        <p><strong>Цена:</strong> {{ jet_ski.price }} ₽</p>
        <p><strong>Описание:</strong> {{ jet_ski.description }}</p>
        <p><strong>Категория:</strong> {{ jet_ski.category.name }}</p>
        <p><strong>ID категории:</strong> {{ jet_ski.category.id }}</p>
        <p><strong>Длина корпуса:</strong> {{ jet_ski.length_hull }} см</p>
        <p><strong>Ширина корпуса:</strong> {{ jet_ski.width_hull }} см</p>
        <p><strong>Вес:</strong> {{ jet_ski.weight }} кг</p>
        <p><strong>Вместимость:</strong> {{ jet_ski.capacity }} чел</p>
        <p><strong>Грузоподъемность:</strong> {{ jet_ski.load_capacity }} кг</p>
        <p><strong>Мощность двигателя:</strong> {{ jet_ski.engine_power }} л.с.</p>
        <p><strong>Объем двигателя:</strong> {{ jet_ski.engine_displacement }} куб.см</p>
        <p><strong>Объем топливного бака:</strong> {{ jet_ski.fuel_capacity }} л</p>
        <p><strong>Материал корпуса:</strong> {{ jet_ski.hull_material }}</p>
        <p><strong>Марка бензина:</strong> {{ jet_ski.gasoline_brand }}</p>
        <h4>Изображения:</h4>
        {% for image in jet_ski.images %}
          <p> <strong>- ID:</strong> {{ image.id }}  <strong>path:</strong> {{ image.path }}</p>
        {% endfor %}
          <p><strong>Дата создания:</strong> {{ jet_ski.created_at | format_datetime }}</p>
          <p><strong>Дата обновления:</strong> {{ jet_ski.updated_at | format_datetime }}</p>
      </div>
    {% endfor %}
  </div>

  <details class="details">
    <summary class="details_title">Добавление Гидроцикла</summary>
    <div class="details_content">
      <h3>Добавление Гидроцикла.</h3>
      <p>Заполните все поля, чтобы добавить гидроцикл. Поле "Название" должно быть уникальным.</p>
      {% if message %}
        <div class="alert {{ 'alert-success' if 'успешно' in message else 'alert-danger' }}">
          <p>{{ message }}</p>
        </div>
      {% endif %}

      <form action="{{ url_for('admin_create_jet_ski') }}" method="post" enctype="multipart/form-data">
        <label for="category_id">ID категории:</label>
        <input type="number" name="category_id" id="category_id" required><br>

        <label for="name">Название:</label>
        <input type="text" name="name" id="name" required><br>

        <label for="price">Цена (руб):</label>
        <input type="number" name="price" id="price" required><br>

        <label for="company_name">Производитель:</label>
        <input type="text" name="company_name" id="company_name" required><br>

        <label for="description">Описание:</label>
        <textarea name="description" id="description"></textarea><br>

        <label for="is_active">Наличие:</label>
        <select name="is_active" id="is_active">
          <option value="true">В наличии</option>
          <option value="false">Нет в наличии</option>
        </select><br>

        <label for="length_hull">Длина корпуса (см):</label>
        <input type="number" name="length_hull" id="length_hull" required><br>

        <label for="width_hull">Ширина корпуса (см):</label>
        <input type="number" name="width_hull" id="width_hull" required><br>

        <label for="weight">Вес (кг):</label>
        <input type="number" name="weight" id="weight" required><br>

        <label for="capacity">Вместимость (чел):</label>
        <input type="number" name="capacity" id="capacity" required><br>
                
        <label for="load_capacity">Грузоподъемность (кг):</label>
        <input type="number" name="load_capacity" id="load_capacity" required><br>
                
        <label for="engine_power">Мощность двигателя (л.с.):</label>
        <input type="number" name="engine_power" id="engine_power" required><br>
                
        <label for="engine_displacement">Объем двигателя (куб.см):</label>
        <input type="number" name="engine_displacement" id="engine_displacement" required><br>
                
        <label for="fuel_capacity">Объем топливного бака (л):</label>
        <input type="number" name="fuel_capacity" id="fuel_capacity" required><br>
                
        <label for="hull_material">Материал корпуса:</label>
        <input type="text" name="hull_material" id="hull_material" required><br>
                
        <label for="gasoline_brand">Марка бензина:</label>
        <input type="number" name="gasoline_brand" id="gasoline_brand" required><br>
                
        <label for="images">Изображения (Зажимая "Shift", выберите изображения):</label>
        <input type="file" name="images" id="images" multiple accept="image/*"><br>

        <button type="submit" class="btn-details">Создать гидроцикл</button>
      </form>
    </div>
  </details>

  <details class="details">
    <summary class="details_title">Обновление Данных</summary>
    <div class="details_content">
      <h3>Обновление информации о гидроцикле.</h3>
      <p>Укажите ID гидроцикла и заполните поля, которые хотите изменить.</p>
      {% if message %}
        <div class="alert {{ 'alert-success' if 'успешно' in message else 'alert-danger' }}">
          <p>{{ message }}</p>
        </div>
      {% endif %}

      <form action="{{ url_for('admin_update_jet_ski') }}" method="post">
        <label for="jet_ski_id_up">ID гидроцикла, который нужно обновить:</label>
        <input type="number" name="jet_ski_id_up" id="jet_ski_id_up" required><br>

        <label for="name">Название:</label>
        <input type="text" name="name"><br>

        <label for="price">Цена (руб):</label>
        <input type="number" name="price"><br>

        <label for="company_name">Производитель:</label>
        <input type="text" name="company_name"><br>

        <label for="description">Описание:</label>
        <textarea name="description"></textarea><br>

        <label for="is_active">Наличие:</label>
        <select name="is_active">
          <option value="true">В наличии</option>
          <option value="false">Нет в наличии</option>
        </select><br>

        <label for="length_hull">Длина корпуса (см):</label>
        <input type="number" name="length_hull"><br>

        <label for="width_hull">Ширина корпуса (см):</label>
        <input type="number" name="width_hull"><br>

        <label for="weight">Вес (кг):</label>
        <input type="number" name="weight"><br>

        <label for="capacity">Вместимость (чел):</label>
        <input type="number" name="capacity"><br>
                
        <label for="load_capacity">Грузоподъемность (кг):</label>
        <input type="number" name="load_capacity"><br>
                
        <label for="engine_power">Мощность двигателя (л.с.):</label>
        <input type="number" name="engine_power"><br>
                
        <label for="engine_displacement">Объем двигателя (куб.см):</label>
        <input type="number" name="engine_displacement"><br>
                
        <label for="fuel_capacity">Объем топливного бака (л):</label>
        <input type="number" name="fuel_capacity"><br>
                
        <label for="hull_material">Материал корпуса:</label>
        <input type="text" name="hull_material"><br>
                
        <label for="gasoline_brand">Марка бензина:</label>
        <input type="number" name="gasoline_brand"><br>

        <button type="submit" class="btn-details">Обновить данные</button>
      </form>
    </div>
  </details>

  <details class="details">
    <summary class="details_title">Обновление Фото</summary>
    <div class="details_content">
      <h3>Обновление фотографий гидроцикла</h3>
      <p>Укажите ID гидроцикла, у которого хотите изменить фото. Укажите через запятую, без пробелов, 
          ID изображений этого гидроцикла которые хотите удалить.
      </p>
      <p>Добавьте новые фото, зажимая "Shift", выберите нужные изображения.</p>
      {% if message %}
        <div class="alert {{ 'alert-success' if 'успешно' in message else 'alert-danger' }}">
          <p>{{ message }}</p>
        </div>
      {% endif %}

      <form action="{{ url_for('admin_update_jet_ski_images') }}" method="post" enctype="multipart/form-data">
        <label for="jet_ski_id_img">ID гидроцикла, у которого нужно обновить фото:</label>
        <input type="number" name="jet_ski_id_img" id="jet_ski_id_img" required><br>

        <label for="remove_images">ID изображений для удаления (через запятую, без пробелов):</label>
        <input type="text" name="remove_images" id="remove_images"><br>

        <label for="add_images">Новые изображения (Зажимая "Shift", выберите несколько):</label>
        <input type="file" name="add_images" id="add_images" multiple accept="image/*"><br>

        <button type="submit" class="btn-details">Обновить фото</button>
      </form>
    </div>
  </details>

  <details class="details">
    <summary class="details_title">Удаление Гидроцикла</summary>
    <div class="details_content">
      <h3>Удаление гидроцикла по ID.</h3>
      <p>Укажите ID гидроцикла, который хотите удалить.</p>
      {% if message %}
        <div class="alert {{ 'alert-success' if 'успешно' in message else 'alert-danger' }}">
          <p>{{ message }}</p>
        </div>
      {% endif %}

      <form action="{{ url_for('admin_delete_jet_ski') }}" method="post">
        <label for="jet_ski_id_del">ID гидроцикла:</label>
        <input type="number" name="jet_ski_id_del" id="jet_ski_id_del" required>
         <button type="submit" class="btn-details">Удалить</button>
      </form>
    </div>
  </details>
{% endblock %}
```

## ✅ Итог

**Обновленные HTML-страницы:**
- `templates/products/catalog.html`
- `templates/admin/admin-base.html`

**Созданные HTML-страницы:**
- `templates/products/jet-skis.html`
- `templates/products/jet-ski-detail.html`
- `templates/admin/jet-skis.html`
---
[← Назад в README](../../../README.md)