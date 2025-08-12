# Character Counter API (FastAPI)

Counts characters with Python `len()` (code points), optional bytes and graphemes.

## Deploy on Render
1. Connect this repo in Render → New → Web Service.
2. Build command: `pip install -r requirements.txt`
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. After deploy, note the URL (e.g., `https://charcount-api.onrender.com`).

## Test
POST `/<host>/count` with JSON body:
```json
{"text":"👍🏽👍","include":["pythonLen","graphemes"]}
