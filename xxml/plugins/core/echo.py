from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg

cmd = on_command("echo", priority=10, block=True)

@cmd.handle()
async def handle_function(args: Message = CommandArg()):
    print(1)
    await cmd.send(args.extract_plain_text())