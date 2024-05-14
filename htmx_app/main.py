from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

import uuid
from datetime import timedelta

from websocket_helper import handle_websocket_chat

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    
    context = {
        "request": request,
        "title": "Streaming Chat"
    }

    response = templates.TemplateResponse("base.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=timedelta(days=1))
    return response


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await handle_websocket_chat(websocket)


@app.websocket("/ws_for_testing")
async def websocket_endpoint(websocket: WebSocket):

    return await handle_websocket_chat(websocket)