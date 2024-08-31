import revTongYi.qianwen as qwen
import logging


logging.getLogger().setLevel(logging.INFO)

# 初始化 Chatbot
chatbot = qwen.Chatbot(cookies_str="aui=1519003169429625;_samesite_flag_=true;cna=GdvMHmtl2D4BASoJusFZ4pAT;tfstk=clGGBO99GAy_fdbp-FN6ho4rSklGZgWbqci-Th4weqvLORhFi9WFUnwpeltWbt1..;aliyun_lang=zh;atpsida=10514b09c208726648d24076_1718552237_2;aliyun_site=CN;isg=BISEcR_5vhgcHAqlV2DLObaQVQJ2nagHezvvgp4lIc8SySWTxq3xl3krDGERaOBf;aliyun_country=CN;munb=2217139628587;login_current_pk=1519003169429625;tongyi_sso_ticket=7Uh1WsjaK5MmR9*eIt*trtMUHEnF6AFvL_vsQhJtj_3CMZPPnqglgxyr5a4EOzDL0;_tb_token_=eef3e53887597;cnaui=1519003169429625;cookie2=18a214c666d409461905a22924b5d914;login_aliyunid_pk=1519003169429625;sca=99d0b0a7;t=5b8479def574e262792705445e9974ca;tongyi_guest_ticket=pv74hHq2xpzQh*Mlg0syXHFk9*Kyp*wFVGYX6BG53u2yQcQcUoDW8u8_y$Em4u_DmdbPy9QeNHj20;XSRF-TOKEN=0d0a8d33-2495-4fc4-b6b1-0eb7f7f9cf7b;yunpk=1519003169429625")
if_first = True

prompt = '''
中国花游队望圆梦巴黎'''

resp = chatbot.ask(prompt=prompt)
print(resp)