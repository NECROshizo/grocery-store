# Grocery-store

## Описание
Backend сервис для магазина продуктов.

## Технологии

[![Python](https://img.shields.io/badge/Python-%5E3.12-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Latest-blue?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
-----
[![Django](https://img.shields.io/badge/Django-%5E5.0.6-blue?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django Rest Framework](https://img.shields.io/badge/DjangoRestFramework-%5E3.15.1-blue?style=flat&logo=django&logoColor=white)](https://pypi.org/project/djangorestframework/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%5E22.0.0-blue?style=flat&logo=gunicorn&logoColor=white)](https://pypi.org/project/gunicorn/)
-----
[![Ruff](https://img.shields.io/badge/Ruff-used-green?style=flat)](https://pypi.org/project/ruff/)
[![Pre-commit](https://img.shields.io/badge/Pre--commit-used-green?style=flat&logo=pre-commit&logoColor=white)](https://pypi.org/project/pre-commit/)

## Требования
<details>
  <summary>Чек лист с требованиями</summary>

- [x] **Управление категориями и подкатегориями**
  - [x] Должна быть реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в админке.
  - [x] Категории и подкатегории обязательно должны иметь наименование, slug-имя, изображение.
  - [x] Подкатегории должны быть связаны с родительской категорией.
  - [x] Должен быть реализован эндпоинт для просмотра всех категорий с подкатегориями. Должна быть предусмотрена пагинация.

- [x] **Управление продуктами**
  - [x] Должна быть реализована возможность добавления, изменения, удаления продуктов в админке.
  - [x] Продукты должны относится к определенной подкатегории и, соответственно, категории. Должны иметь наименование, slug-имя, изображение в 3-х размерах, цену.
  - [x] Должен быть реализован эндпоинт вывода продуктов с пагинацией. Каждый продукт в выводе должен иметь поля: наименование, slug, категория, подкатегория, цена, список изображений.

- [x] **Корзина**
  - [x] Реализовать эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
  - [x] Реализовать эндпоинт вывода состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
  - [x] Реализовать возможность полной очистки корзины.

- [x] **Права доступа**
  - [x] Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь.
  - [x] Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной.

- [x] **Авторизация**
  - [x] Реализовать авторизацию по токену.

- [x] **Дополнительно**
  - [x] Подключенны pre-commit.
  - [x] Настроен линтер ruff.
  - [x] Реализованна возможность добавлять товары списком.
  - [x] Реализован запуск проекта в Docker.

</details>

## Запуск проекта
### Запуск локально с помощью Docker
1. Клонировать репозиторий.
    ```bash
    git clone git@github.com:NECROshizo/grocery-store.git
    cd grocery-store
    ```

2. Создайте и заполните файл `.env` согласно шаблону [.env.example](https://github.com/NECROshizo/grocery-store/blob/develop/infra/.env.example).

3. Перейдите в директорию `infra` и соберите и запустите контейнеры с помощью Docker Compose.
    ```bash
    cd infra
    docker-compose -f docker-compose.local.yaml up --build
    ```

4. Для остановки контейнеров используйте команду:
    ```bash
    docker-compose -f docker-compose.local.yaml down
    ```

Теперь ваш проект запущен.
### Настройка и запуск локально для разработки
Проект использует [Poetry](https://python-poetry.org/) как инструмент управления зависимостями.

1. Клонировать репозиторий.
    ```bash
    git clone git@github.com:NECROshizo/grocery-store.git
    cd diary-workout-tracker-backend
    ```

2. Создание и активация виртуального окружения при помощи [Poetry](https://python-poetry.org/docs/#installation).

    2.1 Создание отдельного окружения:
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
    для Linux и macOS:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    2.2 Использование Poetry:
    ```bash
    pip install poetry
    poetry shell
    poetry install
    ```
> **Примечание:** версия Python должна быть ^3.12.

3. Инициализация pre-commit.
    ```bash
    poetry run pre-commit install
    ```

4. Создайте и заполните файл `.env` согласно шаблону [.env.example](https://github.com/NECROshizo/grocery-store/blob/develop/infra/.env.example).

5. Сапуск postgresql(при необходимости):
  ```bash
  cd infra/
  docker-compose -f docker-compose.local.yaml up --build
  cd ..
  ```

6. Запустите проект с выполнив следующие команды вручную:

    При первом запуске:
    ```bash
    python backend/manage.py migrate
    python backend/manage.py collectstatic --noinput
    ```

    Для последующих запусков:
    ```bash
    python backend/manage.py runserver
    ```

Теперь ваш проект должен быть настроен и готов к локальной разработке.


## Описание эндпоинтов

### Эндпоинты авторизации (JWT)

<details>
  <summary>Создание пользователя (POST /auth/users/)</summary>

  *Регистрация нового пользователя.*

  **Request:**

  ```json
  {
    "username": "user1",
    "password": "password123",
    "email": "user1@example.com"
  }
  ```

  **Response:**

  ```json
  {
    "email": "user1@example.com",
    "username": "user1",
    "id": 1
  }
  ```

  **Status Code: 201 CREATED**
</details>

<details>
  <summary>Получение JWT токена (POST /auth/jwt/create/)</summary>

  *Получение JWT токена для авторизации.*

  **Request:**

  ```json
  {
    "username": "user1",
    "password": "password123"
  }
  ```

  **Response:**

  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Обновление JWT токена (POST /auth/jwt/refresh/)</summary>

  *Обновление просроченного JWT токена.*

  **Request:**

  ```json
  {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

  **Response:**

  ```json
  {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Проверка JWT токена (POST /auth/jwt/verify/)</summary>

  *Проверка действительности JWT токена.*

  **Request:**

  ```json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  ```

  **Response:**

  ```json
  {
    "detail": "Token is valid"
  }
  ```

  **Status Code: 200 OK**
</details>

### Эндпоинты приложения

<details>
  <summary>Получение категорий (GET /api/v1/categories/)</summary>

   *Получение списка всех категорий.*

> **Авторизация не требуется**

  **Response:**

  ```json
  {
	"count": 2,
	"next": null,
	"previous": null,
	"results": [
	  {
		"title": "Категория 1",
		"slug": "kategoriya-1",
		"subcategories": [
		  {
			"title": "Подкатегория 1",
			"slug": "podkategoriya-1",
			"image": "http://example.com/media/image.jpg"
		  },
		  {
			"title": "Подкатегория 2",
			"slug": "podkategoriya-2",
			"image": "http://example.com/media/image.jpg"
		  }
		],
		"image": "http://example.com/media/image.jpg"
	  },
	  {
		"title": "Категория 2",
		"slug": "kategoriya-2",
		"subcategories": [],
		"image": "http://example.com/media/image.jpg"
	  }
	]
  }
  ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Получение продуктов (GET /api/v1/products/)</summary>

  *Получение списка всех продуктов.*

  >  **Авторизация не требуется**

  **Response:**

  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "title": "Продукт 1",
        "price": "100.00",
        "slug": "produkt-1",
        "category": {
          "title": "Категория 1",
          "slug": "kategoriya-1",
          "image": "http://example.com/media/image.jpg"
        },
        "subcategory": {
          "title": "Подкатегория 1",
          "slug": "podkategoriya-1",
          "image": "http://example.com/media/image.jpg"
        },
        "images": [
          "http://example.com/media/original_image.jpg",
          "http://example.com/media/medium_image.jpg",
          "http://example.com/media/small_image.jpg"
        ]
      },
      {
        "title": "Продукт 2",
        "price": "50.00",
        "slug": "produkt-2",
        "category": {
          "title": "Категория 2",
          "slug": "kategoriya-2",
          "image": "http://example.com/media/image.jpg"
        },
        "subcategory": {
          "title": "Подкатегория 2",
          "slug": "podkategoriya-2",
          "image": "http://example.com/media/image.jpg"
        },
        "images": [
          "http://example.com/media/original_image.jpg",
          "http://example.com/media/medium_image.jpg",
          "http://example.com/media/small_image.jpg"
        ]
      }
    ]
  }
  ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Получение корзины (GET /api/v1/shopping-cart/)</summary>

  *Получение списка продуктов в корзине текущего пользователя с суммарной информацией о количестве товаров в корзине и общей стоимости всех товаров*

  > **Требуется авторизация по JWT-токену**

  **Response:**

  ```json
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "product": {
          "title": "Продукт 1",
          "price": "100.00",
          "slug": "produkt-1",
          "category": {
            "title": "Категория 1",
            "slug": "kategoriya-1",
            "image": "http://example.com/media/image.jpg"
          },
          "subcategory": {
            "title": "Подкатегория 1",
            "slug": "podkategoriya-1",
            "image": "http://example.com/media/image.jpg"
          },
          "images": [
            "http://example.com/media/original_image.jpg",
            "http://example.com/media/medium_image.jpg",
            "http://example.com/media/small_image.jpg"
          ]
        },
        "count": 2
      },
      {
        "product": {
          "title": "Продукт 2",
          "price": "50.00",
          "slug": "produkt-2",
          "category": {
            "title": "Категория 2",
            "slug": "kategoriya-2",
            "image": "http://example.com/media/image.jpg"
          },
          "subcategory": {
            "title": "Подкатегория 2",
            "slug": "podkategoriya-2",
            "image": "http://example.com/media/image.jpg"
          },
          "images": [
            "http://example.com/media/original_image.jpg",
            "http://example.com/media/medium_image.jpg",
            "http://example.com/media/small_image.jpg"
          ]
        },
        "count": 1
      }
    ],
    "summary": {
      "total_items": 3,
      "total_price": "250.00"
    }
  }


 ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Добавление в корзину (POST /api/v1/shopping-cart/)</summary>

   *Добавление продуктов в корзину текущего пользователя. При наличие товара в корзине добавленные товары суммируются к тому количеству что уже есть.*

>  **Требуется авторизация по JWT-токену**

  **Request:**

  ```json
  {
    "products": [
      {
        "product": "produkt-1",
        "count": 2
      },
      {
        "product": "produkt-2",
        "count": 1
      }
    ]
  }
  ```

  **Response:**

  ```json
  {
    "result": "success"
  }
  ```

  **Status Code: 201 CREATE**
</details>

<details>
  <summary>Обновление корзины (PATCH/PUT /api/v1/shopping-cart/)</summary>

   *Обновление количества продуктов в корзине текущего пользователя. При наличие товара в корзине его количество обновляется на переданное*

   >  **Требуется авторизация по JWT-токену**

  **Request:**

  ```json
  {
    "products": [
      {
        "product": "produkt-1",
        "count": 3
      },
      {
        "product": "produkt-2",
        "count": 1
      }
    ]
  }
  ```

  **Response:**

  ```json
  {
    "result": "success"
  }
  ```

  **Status Code: 200 OK**
</details>

<details>
  <summary>Удаление из корзины (DELETE /api/v1/shopping-cart/)</summary>

  *Удаление продуктов из корзины текущего пользователя. При наличие товара в корзине его количество уменьшится на переданное количество, если количество снижается до 0, то товар удаляется из корзины*

  >  **Требуется авторизация по JWT-токену**

  **Request:**

  ```json
  {
    "products": [
      {
        "product": "produkt-1",
        "count": 1
      },
      {
        "product": "produkt-2",
        "count": 1
      }
    ]
  }
  ```

  **Response:**

  ```json
  {
    "result": "success"
  }
  ```

  **Status Code: 204 NO CONTENT**
</details>

<details>

  <summary>Очистка корзины (DELETE /api/v1/shopping-cart/clear/)</summary>

  *Полная очистка корзины текущего пользователя.*

  >  **Требуется авторизация по JWT-токену**

  **Response:**

  ```json
  {
    "result": "success"
  }
  ```

  **Status Code: 204 NO CONTENT**
</details>
