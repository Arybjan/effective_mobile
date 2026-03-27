# Custom Authentication & Authorization System

Backend-приложение с собственной системой аутентификации и авторизации, реализованной без полной опоры на встроенные механизмы фреймворка

## Описание проекта

В проекте реализованы:

- регистрация пользователя
- вход в систему по email и паролю
- выход из системы
- обновление профиля
- мягкое удаление аккаунта
- идентификация пользователя по JWT-токену
- собственная ролевая система доступа (RBAC)
- проверка доступа к ресурсам по ролям и разрешениям
- mock business resources для демонстрации авторизации

## Разница между аутентификацией и авторизацией

### Аутентификация
Аутентификация отвечает на вопрос: **кто это?**

```
В проекте аутентификация реализована через:
- email + password
- bcrypt для хранения паролей в виде хеша
- JWT access token
- custom authentication class, которая определяет пользователя по заголовку:
```

```http
Authorization: Bearer <token>
```

### Авторизация

Авторизация отвечает на вопрос: **что этому пользователю разрешено делать?**

В проекте авторизация реализована через:
```
- роли пользователей
- бизнес-ресурсы
- правила доступа для каждой роли к каждому ресурсу
```

```
Используемые технологии
Python
Django
Django REST Framework
PostgreSQL
bcrypt
PyJWT
python-dotenv
```

### Архитектура проекта
```
auth_system/
├── apps/
│   ├── accounts/
│   ├── access/
│   └── mock_resources/
├── common/
├── config/
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
├── .env
├── .env.example
├── manage.py
└── README.md
```

### Структура приложений

```apps/accounts

Отвечает за:

регистрацию
логин
логаут
профиль пользователя
soft delete аккаунта
хранение пользовательских сессий
```

```apps/access

Отвечает за:

роли
бизнес-ресурсы
правила доступа
проверку прав
API для администратора
```

```apps/mock_resources

Содержит mock endpoints для демонстрации того, как работает система авторизации.

common

Содержит:

JWTAuthentication
bcrypt / jwt utils
общие исключения
```

### Схема базы данных
```Таблица users

Хранит пользователей системы.

Поля:

id
first_name
last_name
middle_name
email
password_hash
role_id
is_active
created_at
updated_at
deleted_at
```

```Таблица user_sessions

Хранит активные пользовательские сессии.

Поля:

id
user_id
token
is_active
created_at
expires_at
```

```Таблица roles

Хранит роли пользователей.

Примеры:

admin
manager
user
```

```Таблица business_elements

Хранит ресурсы приложения.

Примеры:

users
products
orders
access_rules
```

```Таблица access_role_rules

Хранит правила доступа роли к определенному ресурсу.

Поля:

role_id
element_id
read_permission
read_all_permission
create_permission
update_permission
update_all_permission
delete_permission
delete_all_permission
```

### Логика прав доступа
#### Основная идея

Для каждой роли задаются права на конкретный ресурс.

Например:
```
read_permission=True — пользователь может читать только свои объекты
read_all_permission=True — пользователь может читать все объекты
update_permission=True — может изменять только свои объекты
update_all_permission=True — может изменять любые объекты
```
Коды ответов
```
401 Unauthorized — пользователь не аутентифицирован
403 Forbidden — пользователь аутентифицирован, но не имеет прав
200 OK — успешный запрос
201 Created — ресурс успешно создан
400 Bad Request — ошибка валидации
404 Not Found — объект не найден
```

### Реализованные endpoint'ы
```Accounts
Регистрация

POST /api/accounts/register/

Вход

POST /api/accounts/login/

Выход

POST /api/accounts/logout/

Получить свой профиль

GET /api/accounts/me/

Обновить профиль

PATCH /api/accounts/me/

Мягкое удаление аккаунта

DELETE /api/accounts/me/delete/
```

```Access
Получить список ролей

GET /api/access/roles/

Получить список ресурсов

GET /api/access/elements/

Получить список правил

GET /api/access/rules/

Создать правило

POST /api/access/rules/

Обновить правило

PATCH /api/access/rules/<id>/

Доступ к этим endpoint’ам имеет только пользователь с ролью admin.
```

```Mock resources
Список товаров

GET /api/mock/products/

Создать товар

POST /api/mock/products/

Список заказов

GET /api/mock/orders/

Создать заказ

POST /api/mock/orders/

Изменить заказ

PATCH /api/mock/orders/

Удалить заказ

DELETE /api/mock/orders/

Список пользователей

GET /api/mock/users/
```

### Пример работы аутентификации
```
После успешного логина сервер возвращает:

{
  "message": "Успешный вход в систему.",
  "access_token": "jwt_token_here",
  "token_type": "Bearer"
}
```
```
Далее для защищенных endpoint’ов нужно передавать заголовок:

Authorization: Bearer jwt_token_here
Пример работы авторизации

Если обычный пользователь пытается изменить чужой заказ, API возвращает:

{
  "detail": "У вас нет доступа к изменению orders."
}
```

Если администратор запрашивает список правил доступа:
```
GET /api/access/rules/

он получает успешный ответ, так как его роль имеет соответствующие разрешения.
```

### Подготовка окружения
```
Создать файл .env на основе .env.example.

Пример .env:

SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

POSTGRES_DB=auth_system_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```
### Установка и запуск

1. Клонировать проект
```bash
git clone <repo_url>
cd auth_system
```
2. Создать виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate
```
3. Установить зависимости
```bash
pip install -r requirements.txt
```
4. Создать .env

Заполнить переменные окружения по примеру из .env.example

5. Применить миграции
```bash
python manage.py makemigrations
python manage.py migrate
```
6. Создать тестовые роли и правила

Через shell или fixtures.

7. Запустить сервер
```bash
python manage.py runserver
```

### Тестовые роли

admin

Имеет полный доступ ко всем ресурсам и к управлению правилами.

manager

Имеет расширенный доступ к orders и products.

user

Имеет доступ только к собственным данным и собственным заказам, а также может читать товары.

### Что было реализовано самостоятельно

В рамках задания самостоятельно реализованы:

хранение паролей через bcrypt
генерация JWT-токенов
идентификация пользователя через custom authentication class
логика logout через деактивацию сессии
собственная таблица ролей
собственная таблица ресурсов
собственная таблица правил доступа
собственная логика проверки прав доступа
Итог:

различий между аутентификацией и авторизацией
работы JWT
организации пользовательских сессий
ролевой модели доступа
проектирования структуры backend-приложения и БД