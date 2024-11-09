import nonebot
from nonebot.adapters.console import Adapter as ConsoleAdapter
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

from os import path

# 初始化 NoneBot
nonebot.init()

# 注册适配器
driver = nonebot.get_driver()
# driver.register_adapter(ConsoleAdapter)
driver.register_adapter(OnebotV11Adapter)

# 在这里加载插件
# nonebot.load_builtin_plugins("echo")
nonebot.load_plugins("xxml/plugins/core")


if __name__ == "__main__":
    nonebot.run()