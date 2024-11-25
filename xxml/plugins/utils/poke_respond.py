from nonebot import on_notice
from nonebot.adapters import Message, Event, Bot

from nonebot.adapters.onebot.v11 import Message, MessageSegment, PokeNotifyEvent

async def is_poke(event: Event, bot: Bot) -> bool:
    return isinstance(event, PokeNotifyEvent) and (str(event.target_id) == str(bot.self_id))

matcher = on_notice(
    rule=is_poke,
    priority=10, 
    block=True
)

import random

@matcher.handle()
async def handle(event: Event):
    responseTextList = [
        "咬)",
        "？",
        "干森魔？",
        "嗷？",
        "有事吗！",
        "别整 刺挠"
    ]

    await matcher.send(message = Message([
        MessageSegment.at(event.user_id),
        MessageSegment.text(f" {random.choice(responseTextList)}")
    ]))
    pass
    