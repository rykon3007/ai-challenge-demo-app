import os
import chainlit as cl
from chainlit.server import app
from fastapi import Request
from fastapi.responses import (
    HTMLResponse,
)

import requests


@app.get("/test")
def hello(request: Request):
    print(request.headers)
    return HTMLResponse("Hello World")

@app.get("/openai")
def hello(request: Request):
    print(request.headers)
    return HTMLResponse("Hello World")

@cl.on_message
async def main(message: cl.Message):

    hostname = os.environ["HOSTNAME"]

    r = requests.get("http://localhost:8000/test")
    print(r.text)
    await cl.Message(
        content=f"API Received: {r.text}",
    ).send()


