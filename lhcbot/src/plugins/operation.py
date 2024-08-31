import json
import time
from typing import Union, Optional, List

import nonebot
from nonebot.rule import Rule
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message, on_request
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent, PrivateMessageEvent, FriendRequestEvent, \
    GroupRequestEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER
from nonebot.permission import SUPERUSER, Permission
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot.params import ArgPlainText, CommandArg, ArgStr
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent, Event, escape, ActionFailed


def At(data: str) -> Union[list[str], list[int], list]:
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json()  event: GroupMessageEvent
    :return: list
    """
    try:
        qq_list = []
        data = json.loads(data)
        for msg in data['message']:
            if msg['type'] == 'at':
                if 'all' not in str(msg):
                    qq_list.append(int(msg['data']['qq']))
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []


try:
    with open('admin.json', 'r') as f:
        qq = json.load(f)
except FileNotFoundError:
    qq = 1065200934

abstract = on_keyword({"来到鼠鼠们的小窝"}, priority=30, block=True)


''''@abstract.handle()
async def _(state: T_State, event: GroupMessageEvent):
    at = At(event.json())
    # await abstract.send(str(at))
    if len(at) == 1 and at[0] > 0:
        await abstract.finish(
            MessageSegment.at(at[0]) + MessageSegment.text(
                f' 欢迎新人，加{qq}或管理员发三连截图领取视频对应资源哦！管理员不是机器人，加完请耐心等待。')'''


async def ss(event: GroupMessageEvent) -> bool:
    return event.user_id in [2743218818]


SS: Permission = Permission(ss)
abstract = on_command("加", priority=30, block=True, permission=GROUP_OWNER | SUPERUSER | SS)


@abstract.handle()
async def _(state: T_State, event: GroupMessageEvent, arg: Message = CommandArg()):
    global qq
    if arg.extract_plain_text().strip():
        id = arg.extract_plain_text().strip()
        if id.isdigit() and 10000 < int(id):
            qq = int(id)
            with open('admin.json', 'w') as f:
                json.dump(qq, f, indent=4)
            await abstract.send(MessageSegment.face(124) + '收到')
            return
    at = At(event.json())
    if len(at) == 1 and at[0] > 0:
        qq = at[0]
        with open('admin.json', 'w') as f:
            json.dump(qq, f, indent=4)
        await abstract.send(MessageSegment.face(124) + '收到')
