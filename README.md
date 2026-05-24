# scrape_marketplaces
Загрузка и анализ товаров и цен маркетплейсов.

Здесь представлена конфигурация 1с, которая подключается к сервесу сканирования маркетплейсов. На текущий момент только Ozon.
Подключается и по указанным отборам загружает товары и цены.

На текущий момент сервис в тестовом режиме и бесплатен. Функционал будет развиваться.

Сама конфигурация 1с довольно таки простая, и представляет демонстрацию как загружать товары из сервиса.

Так же товары можно загружать при помощи любых других скриптов.

Пример структуры запроса:
```
{
"search_string": "вкусняшка",
"expected_count_items": 100,
"min_price": 10,
"max_price": 1000,
"sorting": "Популярные"
}
```
(там еще можно указать url_category)

Пример ответа сервера:
```
[
    {
        "src_sku": "2759136519",
        "href": "/product/kislye-konfety-drazhe-vkus-fruktovyy-2759136519/?at=VvtzE6pyLHogLq4XhnLgW6YsPQDMwmFyqjojECOBRgJW",
        "href0": "kislye-konfety-drazhe-vkus-fruktovyy-2759136519",
        "badges": [
            "Распродажа",
            "Стало дешевле"
        ],
        "src_price": "45 ₽",
        "src_price_fake": "55 ₽",
        "title": "Кислые конфеты драже. Вкус фруктовый",
        "src_rating": "4.9",
        "src_count_feedbacks": "8 971",
        "brand": null,
        "src_residue": null,
        "delivery": [
            "Завтра"
        ],
        "i_page": 1,
        "i_row": 1,
        "i_order": 8,
        "sku": 2759136519,
        "url": "https://www.ozon.ru/product/kislye-konfety-drazhe-vkus-fruktovyy-2759136519/?at=VvtzE6pyLHogLq4XhnLgW6YsPQDMwmFyqjojECOBRgJW",
        "badge": "Распродажа,Стало дешевле",
        "deliveryInfo": "Завтра",
        "reviewCount": 8971,
        "rating": 4.9,
        "price": 45,
        "price_fake": 55,
        "residue": 0
    },
    ...
```

Чуть позже выложу пример запроса на питоне.
