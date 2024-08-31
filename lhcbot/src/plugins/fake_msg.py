from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, PrivateMessageEvent, GroupMessageEvent
from nonebot_plugin_imageutils import Text2Image, BuildImage
from nonebot_plugin_imageutils.fonts import Font
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import re, base64, httpx
from typing import Union, List
import logging
import asyncio
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_if_fakemsg(bot: Bot, event: Union[GroupMessageEvent, PrivateMessageEvent]) -> bool:
    # 检测消息中是否包含特定格式的伪造消息
    if any(seg.type == 'text' and re.match(r"^\d{6,10}说", seg.data["text"]) for seg in event.message):
        return True
    return False

fake_msg = on_message(rule=check_if_fakemsg, priority=5, block=True)

@fake_msg.handle()
async def handle(bot: Bot, event: Union[PrivateMessageEvent, GroupMessageEvent]):
    logging.info("正在伪造......")
    tasks = []
    
    for seg in event.message:
        if seg.type == 'text':
            user_msgs = re.split(r'\||\+', seg.data['text'])
            tasks.extend([process_user_msg(bot, msg) for msg in user_msgs])
    
    dialogs = await asyncio.gather(*tasks)
    dialogs = [d for d in dialogs if d is not None]

    if not dialogs:
        logging.info("生成对话框失败")
        return

    final_image = combine_dialogs(dialogs)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        final_image.save(temp_file.name)
        with open(temp_file.name, "rb") as im:
            img_bytes = im.read()
            base64_str = "base64://" + base64.b64encode(img_bytes).decode()
            msg = MessageSegment.image(base64_str)
            await bot.send(event, msg)

async def process_user_msg(bot: Bot, user_msg: str) -> Union[Image.Image, None]:
    qq_account = user_msg.split("说", 1)[0].strip()
    if qq_account.isdigit():
        qq = qq_account
    else:
        matches = re.match(r"^\[CQ:at,qq=(\d{6,10})\]$", qq_account)
        if matches:
            qq = matches.group(1)
        else:
            logger.warning(f"无法识别的QQ号或at: {qq_account}")
            return None

    msgs = user_msg.split("说", 1)[1].split(' ')

    try:
        stranger_info = await bot.call_api("get_stranger_info", user_id=int(qq))
        nickname = stranger_info.get("nickname", "QQ用户")
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        nickname = "QQ用户"

    try:
        head_img = await get_head_image(qq)
    except Exception as e:
        logger.error(f"获取头像失败: {e}")
        head_img = Image.new('RGBA', (200, 200), (200, 200, 200, 255))

    dialogs = [await make_dialog(head_img, nickname, msg) for msg in msgs if msg.strip()]
    return combine_dialogs(dialogs) if dialogs else None

async def get_head_image(qq: str) -> Image.Image:
    img_url = f"http://q.qlogo.cn/headimg_dl?dst_uin={qq}&spec=640&img_type=jpg"
    async with httpx.AsyncClient() as client:
        response = await client.get(img_url)
        content = response.content
    head_img = Image.open(BytesIO(content))
    head_img = head_img.convert("RGBA")

    target_size = (100, 100)
    head_img = head_img.resize(target_size)

    mask = Image.new('L', target_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + target_size, fill=255)

    head_img.putalpha(mask)
    return head_img

async def make_dialog(headimg: Image.Image, nickname: str, msg: str) -> Image.Image:
    corner1 = BuildImage.open("src\\corner1.png").convert("RGBA")
    corner2 = BuildImage.open("src\\corner2.png").convert("RGBA")
    corner3 = BuildImage.open("src\\corner3.png").convert("RGBA")
    corner4 = BuildImage.open("src\\corner4.png").convert("RGBA")
    label = BuildImage.open("src\\label.png").convert("RGBA")


    name_img = Text2Image.from_text(nickname, 28, fill="#868894").to_image()
    name_w, name_h = name_img.size

    text_img = Text2Image.from_text(msg, 40).wrap(600).to_image()
    text_w, text_h = text_img.size
    box_w = max(text_w, name_w + 15) + 140
    box_h = max(text_h + 103, 150)

    box = BuildImage.new("RGBA", (780, box_h))
    box.paste(corner1, (0, 0))
    box.paste(corner2, (0, box_h - 75))
    box.paste(corner3, (text_w + 70, 0))
    box.paste(corner4, (text_w + 70, box_h - 75))
    box.paste(BuildImage.new("RGBA", (text_w, box_h - 40), "white"), (70, 20))
    box.paste(BuildImage.new("RGBA", (text_w + 88, box_h - 150), "white"), (27, 75))
    box.paste(text_img, (70, 17 + (box_h - 40 - text_h) // 2), alpha=True)

    dialog = BuildImage.new("RGBA", (box.width + 130, box.height + 60), "#eaedf4")
    dialog.paste(headimg, (30, 25), alpha=True)
    dialog.paste(box, (130, 60), alpha=True)
    dialog.paste(label, (160, 25))
    dialog.paste(name_img, (260, 25 + (35 - name_h) // 2), alpha=True)

    return dialog.image

def combine_dialogs(dialogs: List[Image.Image]) -> Image.Image:
    total_height = sum(d.height for d in dialogs)
    final_image = Image.new('RGBA', (max(d.width for d in dialogs), total_height), (255, 255, 255, 255))
    y_offset = 0
    for d in dialogs:
        final_image.paste(d, (0, y_offset))
        y_offset += d.height
    return final_image
