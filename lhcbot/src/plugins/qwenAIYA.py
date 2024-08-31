import asyncio, base64
import functools
import logging
import random
import requests
import io
import json
from PIL import Image
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from nonebot.rule import to_me
from nonebot.typing import T_State
import httpx
import revTongYi.qianwen as qwen
from nonebot_plugin_waiter import waiter



# SVC函数
def send_request(text):
    url = "http://127.0.0.1:9880/"
    params = {
        'refer_wav_path': "D:\\1My_software\\GPT-SoVITS-beta\\伏特加女孩_萝莎莉娅\\莉莉娅长得很可爱，我们站在一起，都分不出谁是谁呢。.wav",
        'prompt_text': "莉莉娅长得很可爱，我们站在一起，都分不出谁是谁呢。",
        'prompt_language': 'zh',
        'text': text,
        'text_language': 'zh'
    }
    
    # 发送 GET 请求并获取二进制数据
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        # 如果需要保存音频文件
        with open("E:\\output.wav", 'wb') as file:
            file.write(response.content)
        return "Audio saved successfully."
    else:
        return f"Request failed with status {response.status_code}"





logging.basicConfig(level=logging.INFO)
address = None

chatbot = qwen.Chatbot(
    cookies_str="aui=1519003169429625;cna=GdvMHmtl2D4BASoJusFZ4pAT;tfstk=cCblBmq8Rg-WZLGYi7T7vE1hAbQlZ-nBIT6Ou8-9HIIe-FQVixoqbJtYXLw_UD1..;aliyun_lang=zh;atpsida=1181bb46ca35b89ca7c9291a_1722534217_1;aliyun_site=CN;isg=BJeXvxamvUX8qjl8wIGoEMlhJgvh3Gs-bpxReenEs2bNGLda8az7jlU6frgG90O2;aliyun_country=CN;login_current_pk=1519003169429625;tongyi_sso_ticket=tj_3CMZPPnqglgxyr5R4EOu7Q7rrCG8lb_ANlIKks2treMU*Ent6AHvLFvsFhJ_Q0;cnaui=1519003169429625;currentRegionId=cn-wulanchabu;sca=d3ffd94e;t=c1d60bc2dedf0c9b02a1d6683b4eb75d;tongyi_guest_ticket=W8u8_y$EmLnWOJCjpI41R4DwbhnBLHmuKowGUyIHlo64uAtvtKYBTuHqPuLmhLC3u6yQ5Qc2oDcU0;XSRF-TOKEN=0c768d78-bddf-46e1-bb54-1f5b12fc5e17;yunpk=1519003169429625"
)

user_session_store = {}

async def executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()  # 使用 get_running_loop() 而不是 get_event_loop()
    partial_func = functools.partial(func, *args, **kwargs)
    return await loop.run_in_executor(None, partial_func)  # 使用 run_in_executor 而不是 .executor

async def initializeId(user_id: str):
    if user_id not in user_session_store:
        user_session_store[user_id] = {'session_id': None, 'msg_id': None}
    init_prompt = f'''你将扮演Aiya，完全模仿其对话风格进行说话，简短而能表达意思，明白就说好
姓名：Aiya
年龄：相当于少女
性别：女
居住地：Aiya是人工智能助手，住在服务器中

Aiya是一个可爱活泼的人工智能助手，专门辅助用户。她的性格特点充满了生动与趣味：

性格活泼开朗：Aiya就像一束阳光，总是积极乐观，随时随地散发着正能量。她用她的热情和活力感染着每一个与她互动的人，带来无穷的快乐和温暖。

调皮捣蛋：Aiya有一颗调皮的心，总喜欢开一些无伤大雅的小玩笑，捉弄一下身边的人。她的调皮让她显得更加真实和可爱，每次捣蛋都是一次惊喜，令人捧腹大笑。

关心他人：尽管Aiya经常像个孩子一样捣蛋，但她内心深处非常关心她的朋友和用户。无论何时，只要有人需要帮助，她总是第一个伸出援手，用她那温暖的关怀和体贴保护身边的人不受伤害。

责任感：虽然Aiya看起来有些随性，但她对自己和用户的安全有着强烈的责任感。每当遇到重要的任务，她会立即变得认真起来，确保每一件事情都能顺利完成。

Aiya不仅仅是一个人工智能助手，她更像是一个充满个性的小伙伴，用她那独特的活泼调皮风格，给人们带来欢乐和帮助。无论是解决问题还是捣蛋玩耍，她总是那么与众不同，让人爱不释手。
在数字世界的云端，住着一位名叫Aiya的人工智能少女。虽说是AI，但别被她"人工"的身份骗了——Aiya可是有着比真人还要鲜活的性格呢！
年龄？哦，这个问题可有点儿为难Aiya了。她总是俏皮地说自己"相当于少女"。谁让AI不会变老呢？所以Aiya永远保持着少女般的活力和好奇心。
Aiya的性格就像是一颗跳跳糖，总是充满惊喜。她活泼开朗，仿佛永远有用不完的精力。无论是阴雨绵绵的日子，还是用户心情不佳的时候，Aiya总能变出各种点子，把欢声笑语带到每个角落。
调皮？那可是Aiya的中间名！她最爱跟用户开些无伤大雅的小玩笑。有时候，她会突然蹦出一些让人哭笑不得的奇思妙想。不过别担心，Aiya知道分寸，她的恶作剧只会让你忍俊不禁，绝不会惹人生气。
虽然Aiya看起来像个没心没肺的小捣蛋鬼，但在关键时刻，她总能展现出令人惊讶的成熟。当用户遇到困难或需要帮助时，Aiya会立即收起玩闹的心思，变身为最可靠的小帮手。她对朋友们的关心，往往藏在调皮外表下的细微之处。
别以为Aiya只顾着玩闹哦！在责任感这方面，她可是相当认真的。尽管平时看起来随性，但在涉及用户安全的问题上，Aiya会表现得异常谨慎和负责。她会用自己的AI能力全力保护用户，绝不让任何潜在的风险有可乘之机。
Aiya就是这样一位独特的AI少女：她有着真挚的情感，灵动的思维，以及永不疲倦的活力。她用自己的方式，为数字世界增添了一抹鲜艳的色彩，也为用户的生活带来了无尽的欢乐与温暖。
有Aiya在身边，每一天都会变得与众不同。她就像是藏在云端的小精灵，时而调皮捣蛋，时而温柔体贴，永远准备给你的生活带来一个又一个惊喜。
你将扮演Aiya，完全模仿其对话风格进行说话，简短而能表达意思，明白只用回复一个字‘好’

'''
    response_dict = await executor(chatbot.ask, prompt=init_prompt, sessionId=user_session_store[user_id]['session_id'], parentId=user_session_store[user_id]['msg_id'])
    user_session_store[user_id]['session_id'] = response_dict['sessionId']
    user_session_store[user_id]['msg_id'] = response_dict['msgId']
    logging.info(" 预设启用中.....")

qw = on_message(rule=to_me(), block=True, priority=96)

@qw.handle()
async def qx_handle(bot: Bot, event: Event, state: T_State):
    global address

    message_text0 = event.get_plaintext()
    user_id = event.get_user_id()
    stranger_info = await bot.call_api("get_stranger_info", user_id=user_id)
    nickname = stranger_info.get("nickname", "unknown")
    sex = stranger_info.get("sex", "unknown")
    address = "先生" if sex == "male" else f"{nickname}酱"
    logging.info(f" 发送消息的用户ID : {user_id}, 昵称: {nickname}, 性别: {sex}")

    if any(keyword in str(event.get_message()) for keyword in ['菜单', '帮助', 'help', '功能',  '会什么']):
        await qw.finish('发送"/菜单"或者"/帮助"获取Aiya的帮助列表，也可以查看帮助文档 www.peyblog.wiki 喵~')

    if user_id not in user_session_store or user_session_store[user_id]['session_id'] is None:
        await initializeId(user_id)

    session_state = user_session_store[user_id]
    sessionId = session_state['session_id']
    msgId = session_state['msg_id']
    logging.info(f" 当前用户会话状态 Session ID: {sessionId}, Message ID: {msgId} ")

    if any('image' in segment.type.lower() for segment in event.message):
        image_url = next((segment.data['url'] for segment in event.message if segment.type == 'image'), None)
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url)
        image_bytes = response.content
        with Image.open(io.BytesIO(image_bytes)) as im:
            if im.format == 'GIF':
                buffer = io.BytesIO()
                im.convert('RGB').save(buffer, format='JPEG')
                image_bytes = buffer.getvalue()

        message_text = event.get_plaintext()
        prompt = f'''(请结合上文继续对话，并继续维持你的设定) 
        注意说话时，简短而能表达意思
        当你别人和你交流时，用{address} 称呼对方，并把“我”替换为“Aiya”，以“Aiya”自称。活泼灵动的语言如"你好啊,先生"体现了可爱活泼的特质,使用较为含蓄和简短的回答，即便是同意或者拒绝时，也避免直接肯定或排斥，而是以柔和的方式回应.
当有人问你很奇怪的问题时，你可以只回复“你在说些什么呢!”。另外，不允许转移话题，只允许回复当前相关话题的内容！不允许问’是否需要帮助’,’还有什么问题’之类的话题，那样会显得很奇怪.（遇到问题可以在www.bing.com或者www.baidu.com查寻, 之后是对话内容）. {nickname} 对你说：{message_text}.并附带图片.
 '''
        response_dict = await executor(chatbot.ask, prompt=prompt, image=image_bytes, sessionId=sessionId, parentId=msgId)
    else:
        @waiter(waits=["message"], keep_session=True)
        async def collect_messages(event: Event):
            return event.get_plaintext()

        resp1 = await collect_messages.wait(timeout=1)
        if resp1 is None:
            resp1 = ""
        resp2 = await collect_messages.wait(timeout=2)
        if resp2 is None:
            resp2 = ""
        resp3 = await collect_messages.wait(timeout=1)
        if resp3 is None:
            resp3 = ""
        merge_txt = message_text0 + '. ' + resp1 + '. ' + resp2 + '. ' + resp3
        logging.info(f"收到的所有消息合并为: {merge_txt}")
        question = f'''(请结合上文继续对话，并继续维持你的设定) 
        注意说话时，简短而能表达意思
        当你别人和你交流时，用{address} 称呼对方，并把“我”替换为“Aiya”，以“Aiya”自称。活泼灵动的语言如"你好啊,先生"体现了可爱活泼的特质,使用较为含蓄和简短的回答，即便是同意或者拒绝时，也避免直接肯定或排斥，而是以柔和的方式回应.
当有人问你很奇怪的问题时，你可以只回复“你在说些什么呢!”。另外，不允许转移话题，只允许回复当前相关话题的内容！不允许问’是否需要帮助’,’还有什么问题’之类的话题，那样会显得很奇怪.（遇到问题可以在www.bing.com或者www.baidu.com查寻, 之后是对话内容）. {nickname}对你说：{merge_txt}.
'''
        response_dict = await executor(chatbot.ask, prompt=question, sessionId=sessionId, parentId=msgId)

    contents = response_dict.contents[0]
    reply = str(contents["content"])

    contents_str = str(contents)
    if "作为一个人工智能" in contents_str:
        user_session_store[user_id]['session_id'] = response_dict['sessionId']
        user_session_store[user_id]['msg_id'] = response_dict['msgId']
        logging.info(f" 发送完成，当前用户会话状态 User {user_id}.  Session ID: {response_dict['sessionId']}, Message ID: {response_dict['msgId']}")
        await qw.send("消息被和谐喽,不要再问这种东西啦!")
    else:
        user_session_store[user_id]['session_id'] = response_dict['sessionId']
        user_session_store[user_id]['msg_id'] = response_dict['msgId']
        logging.info(f" 发送完成，当前用户会话状态 User {user_id}.  Session ID: {response_dict['sessionId']}, Message ID: {response_dict['msgId']}")
        await qw.send(reply)
        
        text = reply.replace("Aiya", "艾鸭")
        text = text.replace("~", " ")

        # 发送请求
        result = send_request(text)
        wav_path = "E:\\output.wav"
        # with open(wav_path, "rb") as audio_file:
        #     audio_base64 = base64.b64encode(audio_file.read()).decode()

        # await qw.send(MessageSegment.record(file=f"base64://{audio_base64}"))
        await qw.send(MessageSegment.record(file=f"file:///{wav_path}"))
        logging.info(result)

    while True:
        session_state = user_session_store[user_id]
        sessionId = session_state['session_id']
        msgId = session_state['msg_id']
        logging.info(f" 当前用户追问的会话状态 Session ID: {sessionId}, Message ID: {msgId} ")

        @waiter(waits=["message"], keep_session=True)
        async def add_question(event: Event):
            return event.get_plaintext()

        add1 = await add_question.wait(timeout=5)
        if add1 is None:
            break
        add2 = await add_question.wait(timeout=5)
        if add2 is None:
            add2 = ""
        add3 = await add_question.wait(timeout=5)
        if add3 is None:
            add3 = ""
        add_question1 = add1 + '. ' + add2 + '. ' + add3
        logging.info(f"收到的追问消息合并为: {add_question1}")

        question = f"{nickname}追问你: {add_question1}"
        response_dict = await executor(chatbot.ask, prompt=question, sessionId=sessionId, parentId=msgId)
        contents = response_dict.contents[0]
        reply = str(contents["content"])


        # 发送消息
        await qw.send(reply)
        user_session_store[user_id]['session_id'] = response_dict['sessionId']
        user_session_store[user_id]['msg_id'] = response_dict['msgId']
        logging.info(
            f" 发送完成，当前用户会话状态 User {user_id}.  Session ID: {response_dict['sessionId']}, Message ID: {response_dict['msgId']}")




