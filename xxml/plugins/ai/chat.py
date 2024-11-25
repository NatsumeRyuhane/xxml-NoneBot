from nonebot import on_message, on_command
from nonebot.adapters import Message, Event, Bot
from nonebot.typing import T_State
from nonebot.rule import to_me

from nonebot.adapters.onebot.v11 import Message, MessageSegment, MessageEvent

matcher = on_message(
    priority=11,
    block=False
)

import random
from typing import List
from xxml.external.chatgpt import chat, ChatContext

context = ChatContext()

@matcher.handle()
async def handle_logger(bot: Bot, event: MessageEvent, state: T_State):
    context.add_message_log("user", str(event.get_message().extract_plain_text()), str(event.sender.nickname), str(event.get_user_id()))
    
    rule = to_me()
    result = await rule(bot, event, state)

    text = event.get_plaintext()
    p = 1

    if ("xxml" in text) or ("小小毛龙" in text):
        p = 70
    if "小毛龙" in text:
        p = 3

    no_msg = [
        "？",
        "*小小毛龙似乎在假装没看见你的消息",
        "*小小毛龙转过身去抖了抖耳朵，看起来没有搭理你的想法",
        "*...看起来小小毛龙没有回应的打算"
    ]


    if result:
        msg = await chat(context)
        
        if msg:
            await matcher.send(
                message = Message([
                    MessageSegment.reply(event.message_id), # type: ignore
                    MessageSegment.text(msg)
                ])
            )
        else:
            await matcher.send(
                message = Message([
                    MessageSegment.reply(event.message_id), # type: ignore
                    MessageSegment.text(random.choice(no_msg))
                ])
            )
    elif random.randint(0, 99) < p:
        msg = await chat(context)
        if msg:
            await matcher.send(msg)

""""""

async def permit(event: Event):
    return str(event.user_id) == "1750157080" # type: ignore

cmd1 = on_command(
    "memory", 
    priority=10, 
    block=True,
    permission=permit
)

@cmd1.handle()
async def handle_function1():
    await cmd1.send(str(context.memory))

cmd2 = on_command(
    "affinity", 
    priority=10, 
    block=True,
    permission=permit
)

@cmd2.handle()
async def handle_function2():
    await cmd2.send(str(context.affinity))