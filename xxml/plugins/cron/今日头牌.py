import PIL.Image
from nonebot import require, get_bot, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Event

matcher = on_command(
    "今日头牌",
    aliases={"jrtp"},
    priority=10, 
    block=True
)

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

import time
from pathlib import Path
import PIL
from io import BytesIO
import pytz
from datetime import datetime, timezone

tz = pytz.timezone("Asia/Shanghai")
imgDir = Path("./xxml/resources/dick/").resolve()


img_dict = {
    0: "绿豆龙",
    1: "米米",
    2: "拉奇",
    3: "小毛龙",
    4: "龙羽",
    5: "土豆龙",
    6: "盐酸",
    7: "小九",
    8: "大九",
    9: "狼犽",
    10: "狼犽（？",
    11: "不是狼犽",
    12: "啸黑",
    13: "江齐",
    14: "伯乐",
    15: "玍子",
    16: "一信",
    17: "豆豆",
    18: "猫小凯",
    19: "熔赭",
    20: "黑曜"
}

import random
import time
from datetime import date

# 权重相等
weights = [1] * 21

def random_index():
    keys = list(img_dict.keys())
    chosen_key = random.choices(keys, weights=weights, k=1)[0]
    return chosen_key

current_date = None
index_cache = None

def get_today_head():
    global current_date, index_cache
    today = date.today()

    if current_date != today:
        current_date = today
        index_cache = random_index()

    return index_cache

def get_index():
    now = time.time()
    now += 8 * 60 * 60
    now -= 8 * 60 * 60
    days = int(now // (24 * 60 * 60))
    return days % 21

def get_image_file():
    image = imgDir / f"{get_index() :03}.png"
    return image.resolve()

@matcher.handle()
async def handle(event: Event):
    with BytesIO() as buffer:
        image = PIL.Image.open(get_image_file()).save(buffer, format="PNG")
        await matcher.send(message = Message([
            MessageSegment.reply(event.message_id), # type: ignore
            MessageSegment.text(f"今天鸽社的头牌是{img_dict[get_index()]}！\n\n"),
            MessageSegment.image(buffer)
        ]))


@scheduler.scheduled_job("cron", hour=8, minute=0, second=0)
async def func():
    bot = get_bot()
    now = datetime.now(tz)

    with BytesIO() as buffer:
        image = PIL.Image.open(get_image_file()).save(buffer, format="PNG")
        await bot.send_group_msg(
            group_id = 484597471,
            message = Message([
                MessageSegment.text(f"{now.year}年{now.month}月{now.day}日鸽社头牌轮换：{img_dict[get_index()]}\n\n"),
                 MessageSegment.image(buffer)
            ])
        )