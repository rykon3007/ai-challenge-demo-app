import base64
import os
import chainlit as cl
from typing import Optional
import requests

from approach import rag_approach

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    if not message.elements:
        res = rag_approach(message.content)
        msg.content = res
        await msg.update()
    else:
        # 画像を取得して、base64エンコーディング    
        images = [file for file in message.elements if "image" in file.mime]
        encoded = base64.b64encode(images[0].content).decode()



