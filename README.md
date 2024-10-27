# # Блогикум

## Технологии:

- Python 3.9.10
- Django 3.2.16
- SQLite

## Установка (Windows):

1. Клонирование репозитория

```
git clone https://github.com/plushevij/django_sprint4-1.git
```

2. Переход в директорию django_sprint4

```
cd django_sprint4-1
```

3. Создание виртуального окружения

```
python -m venv venv
```

4. Активация виртуального окружения

```
source venv/Scripts/activate
```

5. Обновите pip

```
python -m pip install --upgrade pip
```

6. Установка зависимостей

```
pip install -r requirements.txt
```

7. Переход в директорию blogicum

```
cd blogicum
```

8. Применение миграций

```
python manage.py migrate
```

9. Загрузить фикстуры в БД

```
python manage.py loaddata db.json
```

10. Создать суперпользователя

```
python manage.py createsuperuser
```

11. Запуск проекта, введите команду

```
python manage.py runserver
```

12. Отмена

```
Ctrl + C
```

13. Деактивация виртуального окружения

```
deactivate
```