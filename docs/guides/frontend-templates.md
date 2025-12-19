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
Создадим новую страницу администрирования гидроциклов `templates/admin/jet_skis.html`: