# AI Chat Bot MVP

Embed-чатбот для малого бизнеса: FastAPI + Polza.ai + JS-виджет.

## Безопасность

**Перевыпустите API-ключ Polza.ai**, если он когда-либо попадал в чат или репозиторий:
[polza.ai/dashboard/api-keys](https://polza.ai/dashboard/api-keys)

Ключ храните только в `backend/.env` (файл в `.gitignore`).

## Структура

- `backend/` — FastAPI API (`POST /api/chat`, `GET /api/config/{bot_id}`)
- `backend/clients/` — конфиги клиентов (промпт, домены, брендинг)
- `widget/` — embed-виджет для сайта клиента

## Локальный запуск

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # добавьте POLZA_API_KEY
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000  
Health: http://127.0.0.1:8000/health

### 2. Виджет (демо)

Откройте `widget/demo/index.html` в браузере (Live Server или двойной клик).
Либо из папки `widget`:

```bash
npx serve .
```

## Добавление клиента

1. Создайте `backend/clients/{bot-id}.json` по образцу `client-1.json`
2. Укажите `allowed_domains` — домены сайта клиента (для CORS)
3. Заполните `system_prompt` реальными данными бизнеса

**Важно:** `POLZA_API_KEY` храните в Vercel → Project **chat-bot-api** → Settings → Environment Variables.

## Production URLs (текущий деплой)

- **Widget:** https://widget-silk-alpha.vercel.app/widget.js
- **API:** https://chat-bot-api-lovat.vercel.app (Vercel — работает из РФ без VPN)
- **Demo:** https://widget-silk-alpha.vercel.app/demo/production.html

> Railway (`*.railway.app`) из России часто недоступен без VPN. Используйте Vercel для API.

## Встраивание на сайт клиента

```html
<script
  src="https://widget-silk-alpha.vercel.app/widget.js"
  data-bot-id="client-1"
  data-api-url="https://chat-bot-api-lovat.vercel.app"
  defer
></script>
```

## Деплой backend (Vercel)

```bash
cd backend
npx vercel deploy --prod
```

1. [vercel.com](https://vercel.com) → проект **chat-bot-api**
2. Root Directory: `backend`
3. Environment Variables:
   - `POLZA_API_KEY` — ключ Polza.ai
   - `ENV=production`

## Деплой backend (Railway, альтернатива)

Railway может быть недоступен из РФ без VPN. Предпочтительно Vercel (см. выше).

1. [railway.app](https://railway.app) → Deploy from GitHub, Root Directory: `backend`

## Деплой widget (Vercel)

```bash
cd widget
npx vercel
```

Или через Vercel Dashboard: Import repo, Root Directory = `widget`.

## Переменные окружения

| Переменная | Описание |
|------------|----------|
| `POLZA_API_KEY` | Ключ Polza.ai |
| `ENV` | `development` / `production` |
| `CORS_ORIGINS` | Доп. origins через запятую |
| `POLZA_MODEL` | Модель (по умолчанию `openai/gpt-4o-mini`) |
| `RATE_LIMIT_PER_MINUTE` | Лимит запросов на IP (по умолчанию 20) |

## API

### GET /api/config/{bot_id}

Публичный конфиг для виджета (название, цвет, приветствие).

### POST /api/chat

```json
{
  "bot_id": "client-1",
  "message": "Сколько стоит капучино?",
  "history": []
}
```

Ответ:

```json
{
  "reply": "Капучино стоит 220 ₽."
}
```
