# Деплой MVP

Пошаговая инструкция для production. Выполните после установки Python 3.11+ и Git.

## 1. Подготовка репозитория

```bash
git init
git add .
git commit -m "Initial chat bot MVP"
```

Создайте репозиторий на GitHub и выполните `git push`.

## 2. Backend на Railway

1. Откройте [railway.app](https://railway.app) и войдите через GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Выберите репозиторий
4. **Settings** → **Root Directory** → `backend`
5. **Variables** → добавьте:

| Key | Value |
|-----|-------|
| `POLZA_API_KEY` | новый ключ с [polza.ai/dashboard/api-keys](https://polza.ai/dashboard/api-keys) |
| `ENV` | `production` |

6. **Deploy** → дождитесь статуса Success
7. **Settings** → **Networking** → **Generate Domain**
8. Скопируйте URL, например: `https://chat-bot-api-production.up.railway.app`

Проверка:

```bash
curl https://YOUR-API.up.railway.app/health
curl https://YOUR-API.up.railway.app/api/config/client-1
```

## Альтернатива: Render

1. [render.com](https://render.com) → **New** → **Blueprint**
2. Подключите репозиторий (используется `render.yaml` в корне)
3. Укажите `POLZA_API_KEY` при создании сервиса

## 3. Widget на Vercel

1. [vercel.com](https://vercel.com) → **Add New** → **Project**
2. Import GitHub repo
3. **Root Directory** → `widget`
4. **Deploy**
5. URL виджета: `https://your-project.vercel.app/widget.js`

Проверка: откройте в браузере URL `/widget.js` — должен отдаться JS-файл.

## 4. Обновите embed-код

В `widget/embed-snippet.html` замените:

- `YOUR-WIDGET.vercel.app` → ваш Vercel домен
- `YOUR-API.railway.app` → ваш Railway домен

## 5. Локальная разработка (Windows)

Установите Python с [python.org](https://www.python.org/downloads/), затем:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# отредактируйте .env — добавьте POLZA_API_KEY
uvicorn app.main:app --reload
```

Демо-виджет: откройте `widget/demo/index.html` через Live Server в VS Code/Cursor.
