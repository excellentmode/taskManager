# Task Manager

Управление своими задачами через веб-интерфейс.

Веб-приложение на **Vue 3 + Flask + PostgreSQL**.

---

##  Быстрый старт (должны быть установленны Git, Docker, Docker-compose)

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/excellentmode/taskManager.git
   cd taskManager
   ```

2. Запустите приложение:

> Убедитесь, что порты `5173` и `5000` свободны.

   ```bash
   docker-compose up --build
   ```

3. Открой в браузере:

    * Front: [http://localhost:5173](http://localhost:5173)
    * Back (API): [http://localhost:5000](http://localhost:5000)


---

## Технологии проекта

| Слой         | Технологии                                |
|--------------|-------------------------------------------|
| **Фронтенд** | Vue 3, Vue Router, Axios, Bootstrap 5     |
| **Бэкенд**   | Flask, Flask-JWT, Marshmallow, SQLAlchemy |
| **БД**       | PostgreSQL (Docker container)             |
| **Сборка**   | Docker, Docker Compose                    |
| **Тесты**    | Pytest (Flask integration tests)          |

---

## Основной функционал

* **Авторизация и регистрация**
* **Управление задачами (Create/Read/Update/Delete)**

---

## Структура проекта

```
.
├── backend/            # Flask API + модели + сервисы
│   └── tests/          # Pytest тесты
├── frontend/           # Vue 3 SPA приложение
│   ├── components/     # Компоненты
│   ├── services/       # Axios-инстанс
│   └── router/         # Маршруты
├── docker-compose.yml  # Docker-сборка
└── README.md
```

---

## Тесты

Запуск тестов бэкенда:

```bash
  pytest
```

---
