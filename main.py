from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    # headers
    headers = dict(request.headers)
    print("📬 Headers recebidos:", headers)

    # body
    data = await request.json()
    print("📩 Body recebido:", data)

    return {"status": "ok"}
