# scrape_marketplaces
Загрузка и анализ товаров и цен маркетплейсов.

## Использование из 1С

Здесь представлена конфигурация 1с, которая подключается к сервесу сканирования маркетплейсов. На текущий момент только Ozon.
Подключается и по указанным отборам загружает товары и цены.

На текущий момент сервис в тестовом режиме и бесплатен. Функционал будет развиваться.

Сама конфигурация 1с довольно таки простая, и представляет демонстрацию как загружать товары из сервиса.

<img width="1114" height="553" alt="2026-05-25_02-06" src="https://github.com/user-attachments/assets/92fff012-72c0-43f6-8783-5e68199f469b" />

Так же товары можно загружать при помощи любых других скриптов.

## Форматы данных

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
(expected_count_items - ограничение максимум 1000)

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

## Использование из других скриптов

В папке python_scripts пример использования на питоне.
В частности в папке python_scripts/results пример выполнения команды:
```
python -m use_cli parameters.json
```

