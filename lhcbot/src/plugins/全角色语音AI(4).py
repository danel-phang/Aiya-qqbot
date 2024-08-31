# python3
# -*- coding: utf-8 -*-
# @Time    : 2024/4/6
# @Author  : 哔哩哔哩鼠鼠
# @Email   : 18545878
# @File    : 全角色语音AI.py
# @Software: PyCharm
import asyncio
import base64
import random
import traceback
from nonebot.exception import FinishedException, ActionFailed
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageEvent, PokeNotifyEvent
from nonebot.adapters.onebot.v11 import GROUP_ADMIN, GROUP_OWNER, GROUP_MEMBER
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.log import logger
from nonebot.params import ArgPlainText, CommandArg, ArgStr
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent, Event, escape
import re
from nonebot.params import CommandArg, ArgStr
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import Event
from nonebot.typing import T_State

roles = ['空', '流萤','荧', '派蒙', '纳西妲', '阿贝多', '温迪', '枫原万叶', '钟离', '荒泷一斗', '八重神子', '艾尔海森',
         '提纳里', '迪希雅', '卡维', '宵宫', '莱依拉', '赛诺', '诺艾尔', '托马', '凝光', '莫娜', '北斗', '神里绫华',
         '雷电将军', '芭芭拉', '鹿野院平藏', '五郎', '迪奥娜', '凯亚', '安柏', '班尼特', '琴', '柯莱', '夜兰', '妮露',
         '辛焱', '珐露珊', '魈', '香菱', '达达利亚', '砂糖', '早柚', '云堇', '刻晴', '丽莎', '迪卢克', '烟绯', '重云',
         '珊瑚宫心海', '胡桃', '可莉', '流浪者', '久岐忍', '神里绫人', '甘雨', '戴因斯雷布', '优菈', '菲谢尔', '行秋',
         '白术', '九条裟罗', '雷泽', '申鹤', '迪娜泽黛', '凯瑟琳', '多莉', '坎蒂丝', '萍姥姥', '罗莎莉亚',
         '留云借风真君', '绮良良', '瑶瑶', '七七', '奥兹', '米卡', '夏洛蒂', '埃洛伊', '博士', '女士', '大慈树王',
         '三月七', '娜塔莎', '希露瓦', '虎克', '克拉拉', '丹恒', '希儿', '布洛妮娅', '瓦尔特', '杰帕德', '佩拉', '姬子',
         '艾丝妲', '白露', '星', '穹', '桑博', '伦纳德', '停云', '罗刹', '卡芙卡', '彦卿', '史瓦罗', '螺丝咕姆', '阿兰',
         '银狼', '素裳', '丹枢', '黑塔', '景元', '帕姆', '可可利亚', '半夏', '符玄', '公输师傅', '奥列格', '青雀',
         '大毫', '青镞', '费斯曼', '绿芙蓉', '镜流', '信使', '丽塔', '失落迷迭', '缭乱星棘', '伊甸', '伏特加女孩',
         '狂热蓝调', '莉莉娅', '萝莎莉娅', '八重樱', '八重霞', '卡莲', '第六夜想曲', '卡萝尔', '姬子', '极地战刃',
         '布洛妮娅', '次生银翼', '理之律者', '真理之律者', '迷城骇兔', '希儿', '魇夜星渊', '黑希儿', '帕朵菲莉丝',
         '天元骑英', '幽兰黛尔', '德丽莎', '月下初拥', '朔夜观星', '暮光骑士', '明日香', '李素裳', '格蕾修', '梅比乌斯',
         '渡鸦', '人之律者', '爱莉希雅', '爱衣', '天穹游侠', '琪亚娜', '空之律者', '终焉之律者', '薪炎之律者',
         '云墨丹心', '符华', '识之律者', '维尔薇', '始源之律者', '芽衣', '雷之律者', '苏莎娜', '阿波尼亚', '陆景和',
         '莫弈', '夏彦', '左然']


def tts(text: str, role: str = '苏莎娜'):

    import requests
    import os
    if role not in roles:
        raise FileNotFoundError
        return ''
    url = f'https://api.lolimi.cn/API/yyhc/y.php?type=2&msg={text}&speaker={role}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }

    response = requests.get(url, headers=headers)

    return response.content


def to_base64(img):
    with open(img, "rb") as im:
        img_bytes = im.read()
    base64_str = "base64://" + base64.b64encode(img_bytes).decode('utf-8')
    return base64_str

abstract = on_command("tts", priority=3, block=True)
@abstract.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["city"] = arg.extract_plain_text().strip()

@abstract.got("text", prompt=f"你想让ta说什么？")
async def _(bot: Bot, event: Event, city: str = ArgStr("city"), text: str = ArgStr("text")):
    try:
        url = f'https://api.lolimi.cn/API/yyhc/y.php?type=2&msg={text}&speaker={city}'
        logger.info(url)
        await abstract.finish(MessageSegment.record(url))


    except FinishedException as e:
        pass
    except ActionFailed as e:
        try:
            result = tts(text=text, role=city)
            logger.info('尝试第二种')
            await asyncio.sleep(random.random() * 2)
            await abstract.finish(MessageSegment.record(result))
        except FinishedException:
            pass
        except ActionFailed:
            try:
                logger.info('尝试第三种')
                await asyncio.sleep(random.random() * 2)
                await abstract.finish(MessageSegment.record(url))
            except FinishedException:
                pass
            except ActionFailed:
                try:
                    logger.info('尝试第四种')
                    await asyncio.sleep(random.random() * 2)
                    await abstract.finish(MessageSegment.record(to_base64(result)))
                except FinishedException:
                    pass
                except ActionFailed:
                    logger.exception(traceback.format_exc())
                    await abstract.finish('语音合成失败，看看是不是没装语音支持')


abstract = on_command("wav", priority=3, block=True)


@abstract.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    if arg.extract_plain_text().strip():
        state["city"] = arg.extract_plain_text().strip()


@abstract.got("city", prompt="你想测试什么音频？")
async def _(bot: Bot, event: Event, city: str = ArgStr("city")):
    await abstract.finish(MessageSegment.record(city))
