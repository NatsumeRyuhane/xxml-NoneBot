from nonebot import on_command
from nonebot.adapters import Message, Event

from nonebot.adapters.onebot.v11 import Message, MessageSegment

matcher = on_command(
    "吃啥",
    priority=10, 
    block=True
)

from pathlib import Path
import random

imgDir = Path("./xxml/resources/吃啥/").resolve()

def get_random_image():
    path = imgDir
    images = list(path.glob("*"))
    random_image = random.choice(images)
    return random_image.resolve()
    

@matcher.handle()
async def handle(event: Event):
    await matcher.send(message = Message([
        MessageSegment.reply(event.message_id),
        MessageSegment.text("我去问了下阿虎，他说可以吃这个!\n\n"),
        MessageSegment.image(f"file:///{get_random_image()}")
    ]))
    pass
    