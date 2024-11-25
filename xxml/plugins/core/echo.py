from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters import Message, Event
from nonebot.params import CommandArg

async def permit(event: Event):
    return str(event.user_id) == "1750157080" # type: ignore

cmd = on_command(
    "echo", 
    priority=10, 
    block=True,
    permission=permit
)

@cmd.handle()
async def handle_function(args: Message = CommandArg()):
    await cmd.send(args.extract_plain_text())