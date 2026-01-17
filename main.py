from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from PIL import Image
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
import random
import re
import json
from html import unescape
from. import tools

@register("随机Leetcode题", "Bury", "随机一道Leetcode题目", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
        tools.update()

    @filter.command("随机一题")
    async def 随机题目(self, event: AstrMessageEvent):
        """随机推荐一个力扣 (LeetCode) 免费题目，并返回格式化字符串
    参数:
        level: 难度级别 (1=简单, 2=中等, 3=困难, "all"=不限)
    返回:
        str: 格式化后的题目信息字符串（含描述、示例、约束等），或错误信息""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)
        yield event.plain_result(tools.随机Leetcode题目(level="all")) # 发送一条纯文本消息

    @filter.command("随机一题1")
    async def 随机题目1(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(tools.随机Leetcode题目(level=1))

    @filter.command("随机一题2")
    async def 随机题目2(self, event: AstrMessageEvent):
        message_str = event.message_str
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(tools.随机Leetcode题目(level=2))
    
    @filter.command("随机一题3")
    async def 随机题目3(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(tools.随机Leetcode题目(level=3))

    @filter.command("完整随机一题")
    async def 完整随机题目(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        message_str = event.message_str
        message_chain = event.get_messages()
        logger.info(message_chain)
        yield event.plain_result(tools.完整随机Leetcode题目(level="all"))

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""




















