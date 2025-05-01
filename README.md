# 🧠 Clanity — Learn Languages with Smart Quizzes

Clanity is an intelligent, file-based language learning Telegram bot built with Python and FastAPI. It helps users expand their vocabulary through interactive quizzes generated from user-uploaded documents.

</br>

## 🔗 Exists "Clanity bot" Telegram link
```bash

@MyWordsHelperBot

```

</br>

## 🚀 Features

- 📄 Upload `.xlsx` files with word translations
- 🧩 Auto-generates quizzes for memorization and testing
- 🔍 Tracks your learning progress
- 🌐 Supports any languages
- 🤖 Telegram bot interface for convenient interaction

</br>

## 📸 Screenshots

*(Coming soon: Add Telegram bot screenshots here)*

</br>

## 📦 Tech Stack

- **Python 3.11**
- **SQLAlchemy** – database ORM
- **PostgreSQL** – database service
- **Alembic** – database migrations tool
- **Pydantic** – data validation
- **MinIO** - storage service
- **Aiogram** – Telegram bot framework


</br>

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YehorVoitenko/Clanity.git
cd Clanity
```

### 2. Run project with docker-compose

``` bash
docker-compose up --build
```

### 3. Enviroments (.env)
```bash
BOT_TOKEN=token
MINIO_HOST=minio
MINIO_PORT=9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET_NAME=bucket-name

POSTGRES_DB=clanity_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

PG_ADMIN_USERNAME=pgadmin@gmail.com
PG_ADMIN_PASSWORD=password
```

