## Локальный запуск

- Создать файлы `app.dev.env` и `postgres.dev.env` из их `.example` версий
- Запустить стек: `docker compose -f docker-sompose.dev.yml up -d`
- Остановить стек: `docker compose -f docker-sompose.dev.yml up -d`
- Подключиться к контейнеру приложения: `docker exec -it gorbushka_app bash`
- Подключиться к контейнеру БД: `docker exec -it gorbushka_db bash`
- Логи приложения: `docker logs -f gorbushka_app`
- Логи БД: `docker logs -f gorbushka_db`