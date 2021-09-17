#!/usr/bin/env python
from entrypoint import get_bots
import os
import shutil

def delete_screen(screen_name):
    os.system(f"screen -S {screen_name} -X quit")


def cleanup(*args):
    for arg in args:
        try:
            shutil.rmtree(arg)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    input("Các màn hình gnu đang chạy tất cả các chương trình của bots.yml sẽ bị dừng! ↵")
    input("Các thư mục bộ nhớ đệm của mỗi bot sẽ bị xóa ↵")
    for botname in get_bots().keys():
        delete_screen(botname)
        cleanup(botname)
