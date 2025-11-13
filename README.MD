# Тестовое задание для компании МКК Луна

## Запуск приложения

```cmd
docker-compose up --build -d
```

## Проведение миграций
```cmd
docker-compose exec web alembic upgrade heads
```

## Заполнение тестовыми данными 
```cmd
docker-compose exec web python /app/scripts/generate_data.py
```

Описание всех запросов можно найти в swagger. Swagger доступен по адресу http://localhost:8080/swagger