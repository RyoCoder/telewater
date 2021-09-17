""" This module defines the constants or default values.
"""
from pydantic import BaseModel, validator
from watermark import Position


class Config(BaseModel):
    watermark: str = "https://raw.githubusercontent.com/RyoCoder/telewater/main/taoanhdep_logo_pornhub.jpg"
    frame_rate: int = 15
    preset: str = "ultrafast"
    position: Position = Position.centre

    @validator("preset")
    def validate_preset(val):
        allowed = ["ultrafast", "fast", "medium", "slow"]
        if not val in allowed:
            raise ValueError(f"Chọn cài đặt trước từ {allowed}")
        return val


START = """I am alive!"""

HELP = """
Sử dụng bot rất đơn giản. Chỉ cần gửi ảnh, video hoặc gif cho bot. Bot sẽ trả lời bằng phương tiện được đánh dấu.

Các lệnh bot `/set` và `/get` có thể đặt và lấy giá trị của các biến cấu hình. Các lệnh rất đơn giản và trực quan. Bot sẽ hiển thị cho bạn cách sử dụng nếu bạn gửi một đối số không chính xác.

Cú pháp cho `/set` ➜  `/set key: value`
Cú pháp cho `/get` ➜  `/get key`

"""

COMMANDS = {
    "start": "khởi động bot hoặc kiểm tra xem còn sống không",
    "set": "đặt giá trị cho một biến cấu hình",
    "get": "biết giá trị của một biến cấu hình",
    "help": "học cách sử dụng bot",
}

config = Config()
