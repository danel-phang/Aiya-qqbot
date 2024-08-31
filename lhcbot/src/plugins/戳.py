import random
from subprocess import run
import json
import requests
import psutil
import os, sys, builtins, threading
import nonebot
from nonebot.rule import Rule
from nonebot import get_driver, on_request, on_notice, on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent, Event, NoticeEvent, GroupDecreaseNoticeEvent, GroupRecallNoticeEvent,PokeNotifyEvent
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg, ArgStr

def _check(event: PokeNotifyEvent):
    return event.target_id == event.self_id

agree_list=[1902059857]

poke=on_notice(rule=_check)

@poke.handle()
async def _(event: PokeNotifyEvent):
    msg = random.choice([
        '哇啊，居然真的有会骚扰AI的变态啊...', '？别戳啦！','欺负AI是会被腐竹ban的！应该会吧...?',
        '(。´・ω・)ん?','别戳啦，再戳5阳光币的'"你再戳！", "？再戳试试？", "别戳了别戳了再戳就坏了555", "我爪巴爪巴，球球别再戳了", 
        "再戳我要报警了！","那...那里...那里不能戳...绝对...", "(。´・ω・)ん?", "有事恁叫我，别天天一个劲戳戳戳！", "欸很烦欸！你戳🔨呢",
        "?", "欺负咱这好吗？这不好", "我希望你耗子尾汁"
        ])
    if(event.user_id in agree_list):
        await poke.finish(Message(f"[CQ:at,qq={event.user_id}]如果是你的话...也不是不行!"))
    else:
        await poke.finish(msg, at_sender=True)
