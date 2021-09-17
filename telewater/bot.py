""" This module defines the functions that handle different events.
"""

from telethon import events
from watermark import File, Watermark, apply_watermark

from telewater import conf
from telewater.utils import cleanup, download_image, gen_kv_str, get_args, stamp


async def start(event):
    await event.respond(conf.START)
    raise events.StopPropagation


async def bot_help(event):
    try:
        await event.respond(conf.HELP)
    finally:
        raise events.StopPropagation


async def set_config(event):

    notes = f"""Lệnh này được sử dụng để đặt giá trị của một biến cấu hình.
    Sử dụng `/set key: val`
    Ví dụ `/set watermark: https://link/to/watermark.png`
    {gen_kv_str()}
    """.replace(
        "    ", ""
    )

    try:
        pos_arg = get_args(event.message.text)
        if not pos_arg:
            raise ValueError(f"{notes}")
        splitted = pos_arg.split(":", 1)

        if not len(splitted) == 2:
            raise ValueError("Định dạng đối số không chính xác")

        key, value = [item.strip() for item in splitted]

        config_dict = conf.config.dict()
        if not key in config_dict.keys():
            raise ValueError(f"Khóa {key} không phải là một khóa hợp lệ trong cấu hình.")

        config_dict[key] = value
        print(config_dict)

        conf.config = conf.Config(**config_dict)

        print(conf.config)
        if key == "watermark":
            cleanup("image.png")
            download_image(url=value)
        await event.respond(f"Giá trị của {key} đã được đặt thành {value}")

    except ValueError as err:
        print(err)
        await event.respond(str(err))
    except Exception as err:
        print(err)

    finally:
        raise events.StopPropagation


async def get_config(event):

    notes = f"""Lệnh này được sử dụng để lấy giá trị của một biến cấu hình.
    Sử dụng `/get key`
    Ví dụ `/get x_off`
    {gen_kv_str()}
    """.replace(
        "    ", ""
    )

    try:
        key = get_args(event.message.text)
        if not key:
            raise ValueError(f"{notes}")
        config_dict = conf.config.dict()
        await event.respond(f"{config_dict.get(key)}")
    except ValueError as err:
        print(err)
        await event.respond(str(err))

    finally:

        raise events.StopPropagation


async def watermarker(event):

    if not (event.gif or event.photo or event.video):
        await event.respond("Tệp không được hỗ trợ.")
        return

    org_file = stamp(await event.download_media(""), user=str(event.sender_id))

    file = File(org_file)
    wtm = Watermark(File("image.png"), pos=conf.config.position)

    out_file = apply_watermark(
        file, wtm, frame_rate=conf.config.frame_rate, preset=conf.config.preset
    )
    await event.client.send_file(event.sender_id, out_file)
    cleanup(org_file, out_file)


ALL_EVENTS = {
    "start": (start, events.NewMessage(pattern="/start")),
    "help": (bot_help, events.NewMessage(pattern="/help")),
    "set": (set_config, events.NewMessage(pattern="/set")),
    "get": (get_config, events.NewMessage(pattern="/get")),
    "watermarker": (watermarker, events.NewMessage()),
}
# this is a dictionary where the keys are the unique string identifier for the events
# the values are a tuple consisting of callback function and event
