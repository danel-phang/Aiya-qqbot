import asyncio
from nonebot.exception import FinishedException, ActionFailed
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupIncreaseNoticeEvent, \
    MessageSegment, Message, GroupMessageEvent, Event, escape
from nonebot.params import CommandArg, ArgStr
from nonebot.typing import T_State
import requests
import random
import base64
import traceback


# 定义牢大TTS函数
def 牢大tts(text: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }
    params = {
        'msg': text,
        #'y': 'EN',
        'type': '2'  # Specify the type here as required by the API
    }
    response = requests.get('https://api.lolimi.cn/API/yyhc/kb.php', params=params, headers=headers)
    return response.content

def to_base64(img):
    with open(img, "rb") as im:
        img_bytes = im.read()
    base64_str = "base64://" + base64.b64encode(img_bytes).decode('utf-8')
    return base64_str

# 定义命令处理器
abstract = on_command("牢大说", priority=3, block=True)

# 处理用户输入的命令和参数
@abstract.handle()
async def handle_input(state: T_State, arg: Message = CommandArg()):
    # 提取命令后紧跟的文字作为待转换的内容
    state["textkebi"] = arg.extract_plain_text().strip()

# 当“text”参数获取到时执行后续逻辑
@abstract.got("textkebi", prompt=f"你想让ta说什么？")
async def generate_tts(bot: Bot, event: Event, text: str = ArgStr("textkebi")):
    try:
        url = f'https://api.lolimi.cn/API/yyhc/kb.php?msg={text}'
        logger.info(url)


        await abstract.finish(MessageSegment.record(url))

    except FinishedException as e:
        pass
    except ActionFailed as e:
        try:
            result = 牢大tts(text=text)
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





