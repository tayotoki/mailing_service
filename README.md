# Описание
Приложение для создания email-рассылок.

## Необходдимо создать файл ```.env```

    # django
    SECRET_KEY=django-insecure-ep0=4xr%ijkm_2jk5y)^-z&r!*k=)^)p!&e74xmte*!%749%2-
    
    # DB
    POSTGRES_DB_NAME=mailing_service
    POSTGRES_USER=postgres
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    POSTGRES_PASSWORD=12345

    # SMTP
    EMAIL_HOST_USER=examle@gmail.com
    APP_PASSWORD=raru rpbt wpsl ulcf # Пароль приложения google (указан пример пароля)

## Необходимые приложения
Для работы приложения локально необходима установка postgresql и redis с запущенными демонами.

## Запуск

    make run

## Регистрация пользователя
При использовании приложения в DEBUG=True режиме, используется консольный бэкенд почтового сервиса.
Поэтому письмо с 4-значным кодом приходит в консоль.