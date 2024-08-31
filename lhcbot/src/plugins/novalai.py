import requests
import io, asyncio
import base64
from PIL import Image
from io import BytesIO
from nonebot.adapters.onebot.v11 import Bot, Event,MessageSegment
from nonebot import on_command, on_startswith, on_keyword, on_fullmatch, on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import MessageSegment
import base64

# 设置 API URL
api_url = "https://api.draw.t4wefan.pub/sdapi/v1/txt2img"

headers = {
    'api': 't4',
}

noval_draw = on_command("n", aliases={"绘画", "nai绘画", "rr"}, block=True, priority=5)
@noval_draw.handle()
async def noval_draw_handle(bot: Bot, event: Event, state: T_State):
    await noval_draw.send("Aiya正在绘画中.........")
    prompt = str(event.get_message()).strip() + ",masterpiece, best quality"

    data = {
        "prompt": prompt,  # 生成图像的描述
        "negative_prompt": "nsfw, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry",  # 排除的提示词（可选）
        "cfg_scale": 10,  # 提示词相关度
        "width": 512,  # 图像宽度
        "height": 512,  # 图像高度
        "denoising_strength": 0.4,  # 去噪强度（可选）
        "steps": 50  # 生成图像的步骤数
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        images = response_data.get("images", [])

        if images:
            for idx, img_str in enumerate(images):
                img_data = base64.b64decode(img_str)
                image = Image.open(io.BytesIO(img_data))
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")  # 或其他格式如PNG
                img_byte_arr = buffered.getvalue()
                img_base64 = "base64://" + base64.b64encode(img_byte_arr).decode()
                msg = MessageSegment.image(img_base64)
                output = await bot.send(event, msg)
                message_id = output['message_id']
                await asyncio.sleep(15)
                await bot.delete_msg(message_id=int(message_id))

    else:
        bot .send("byd出问题了......")

