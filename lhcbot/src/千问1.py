from nonebot import on_message
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from fake_useragent import UserAgent
import revTongYi.qianwen as qwen
import logging
from nonebot_plugin_waiter import waiter

logging.getLogger().setLevel(logging.INFO)

# 初始化 Chatbot
chatbot = qwen.Chatbot(cookies_str="aui=1519003169429625;_samesite_flag_=true;cna=GdvMHmtl2D4BASoJusFZ4pAT;tfstk=clGGBO99GAy_fdbp-FN6ho4rSklGZgWbqci-Th4weqvLORhFi9WFUnwpeltWbt1..;aliyun_lang=zh;atpsida=10514b09c208726648d24076_1718552237_2;aliyun_site=CN;isg=BISEcR_5vhgcHAqlV2DLObaQVQJ2nagHezvvgp4lIc8SySWTxq3xl3krDGERaOBf;aliyun_country=CN;munb=2217139628587;login_current_pk=1519003169429625;tongyi_sso_ticket=7Uh1WsjaK5MmR9*eIt*trtMUHEnF6AFvL_vsQhJtj_3CMZPPnqglgxyr5a4EOzDL0;_tb_token_=eef3e53887597;cnaui=1519003169429625;cookie2=18a214c666d409461905a22924b5d914;login_aliyunid_pk=1519003169429625;sca=99d0b0a7;t=5b8479def574e262792705445e9974ca;tongyi_guest_ticket=pv74hHq2xpzQh*Mlg0syXHFk9*Kyp*wFVGYX6BG53u2yQcQcUoDW8u8_y$Em4u_DmdbPy9QeNHj20;XSRF-TOKEN=0d0a8d33-2495-4fc4-b6b1-0eb7f7f9cf7b;yunpk=1519003169429625")
if_first = True

prompt = '''
你是一个人工智能帮手
'''

def initialize(prompt):
    global chatbot
    resp = chatbot.ask(prompt=prompt)
    logging.info("预设启用......")
    msgId = resp.msgId
    sessionId = resp.sessionId
    return msgId, sessionId

# 创建 Nonebot 事件处理器
qianwen = on_message(rule=to_me())

@qianwen.handle()
async def handle_qianwen(bot: Bot, event: Event):
    global msgId, sessionId, if_first
    logging.info(f"是否为第一次会话: {if_first}")
    if if_first:
        msgId, sessionId = initialize(prompt)
        if_first = False

    message_text1 = event.get_plaintext().strip()

    # 定义 waiter 函数
    @waiter(waits=["message"], keep_session=True)
    async def collect_messages(event: Event):
        return event.get_plaintext()

    resp1 = await collect_messages.wait(timeout=30)
    resp2 = await collect_messages.wait(timeout=30)

    message_text = message_text1 + resp1 +resp2
    logging.info(f"收到的所有消息合并为: {message_text}")

    logging.info(f"当前父会话信息 Session ID: {sessionId}, Message ID: {msgId}")
    resp = chatbot.ask(prompt=message_text, parentId=msgId, sessionId=sessionId)

    # 更新msgId与sessionId
    msgId = resp.msgId
    sessionId = resp.sessionId

    if resp.contents:
        resp_text = resp.contents[0].content
        logging.info(f"发送完成, 当前会话状态 Session ID: {sessionId}, Message ID: {msgId}")
        await qianwen.finish(resp_text)
