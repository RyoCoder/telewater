"""A script to test different aspects of the telewater bot."""

import asyncio
import os
from typing import List

import yaml
from dotenv import load_dotenv
from pydantic import BaseModel
from telethon import TelegramClient

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")


class TestData(BaseModel):
    """Lớp này xác định lược đồ của tệp test.yml"""

    bots: List[str]
    video_file: str


with open("test.yml") as file:
    content = yaml.safe_load(file)

td = TestData(**content)

for items in td.bots:
    print(items)


async def general_test():
    async with TelegramClient("telwater_user", API_ID, API_HASH) as client:
        me = await client.get_me()
        print(f"Đăng nhập với tư cách {me.first_name}")

        message_obj = await client.send_file("me", td.video_file)
        print("Đã tải tệp lên Tin nhắn đã lưu")

        for bot in td.bots:
            await client.send_message(bot, "/start")

        print("Được mời /start cho tất cả các bot")

        for bot in td.bots:
            await client.forward_messages(bot, message_obj)

        print("Đã chuyển tiếp tin nhắn đến các tin nhắn đã lưu")


if __name__ == "__main__":
    asyncio.run(general_test())
