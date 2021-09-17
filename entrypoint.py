#!/usr/bin/env python

"""A command line utility to launch multiple instances of telewater using terminal multiplexer screen"""

import os
import time

import yaml
from dotenv import load_dotenv


def get_bots():
    bots_yml = os.getenv("bots_yml")
    if not bots_yml:
        print("bots_yml env var not found")
        if "bots.yml" in os.listdir():
            with open("bots.yml") as file:
                bots_yml = file.read()
        else:
            print("bot.yml file not found")
            return None

    bots = yaml.full_load(bots_yml)
    print(bots)
    return bots


if __name__ == "__main__":

    load_dotenv()

    bots = get_bots()

    if not bots:
        os.system("telewater")
    else:
        for bot_name, token in bots.items():
            command = f"""screen -dmS {bot_name} bash -c 'telewater -n {bot_name} -t "{token}" ' """
            os.system(command)
            print(f"deployed @{bot_name}")

        print("System up!")
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            print("Các bot sẽ tiếp tục chạy trong nền ngay cả khi bạn chạy CTRL + C")
            print("Để dừng tất cả các bot chạy \n\tpkill screen")
