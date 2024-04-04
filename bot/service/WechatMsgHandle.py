import logging
import re

import requests

from bot.config import config_loader
from bot.infrastructure.wexin import SendMsgNativeApi

log = logging.getLogger(__name__)


class WechatMsgHandle:
    def extract_links(self, text):
        # 定义链接匹配的正则表达式模式
        pattern = r'(https?://\S+)'
        # 使用findall()函数找到所有匹配的链接
        links = re.findall(pattern, text)
        return links

    def handle_user_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml, response_content_body):
        # 如果开启聊天功能

        link = self.extract_links(msgContent)
        if len(link) == 0:
            return

        if len(link) > 1:
            # 链接是多个，不处理
            SendMsgNativeApi.send_text_message_base(wechatId
                                                    , fromWechatId
                                                    , "hey, 一次只能处理一个链接哦"
                                                    , [])
            return
        apiKey = config_loader.loadApiKey()
        try:

            response_content_body = requests.post(f"https://api.wxshares.com/api/qsy/as?key={apiKey}&url={link[0]}",
                                                  timeout=5)
            res_data = response_content_body.json()
        except Exception as e:
            log.error(f"Exception during API call: {e}")
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
            return
        if res_data['code'] != 200:
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
        title = res_data['data']['title']
        url = res_data['data']['url']
        photo = res_data['data']['photo']
        picsList = []
        if 'pics' in res_data['data']:
            picsList = res_data['data']['pics']

        res_content = "标题：\n" + title + "\n\n" + "链接：\n" + url + "\n\n" + "图片：\n" + photo

        if picsList:
            res_content = res_content + "\n" + "更多图片：\n" + "\n".join(picsList)
        SendMsgNativeApi.send_text_message_base(wechatId
                                                , fromWechatId
                                                , res_content
                                                , [])
        return

    def chekAdminMsgFlag(self, wechatId, response_content_body):
        fromWechatId = response_content_body["from"]
        if "@chatroom" in fromWechatId and "chatroomMemberInfo" in response_content_body:
            fromWechatId = response_content_body["chatroomMemberInfo"]["userName"]
        admimnUser = config_loader.getAdminUserName()
        return admimnUser == fromWechatId

    def handle_channel_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml, response_content_body,
                               xml_dict):
        groupId = None
        if "@chatroom" in fromWechatId:
            # 如果是群，则跳过id
            return
        # 不是群、或者配置了去水印，则下载视频并回复
        objectId = xml_dict["msg"]["appmsg"]["finderFeed"]["objectId"]
        objectNonceId = xml_dict["msg"]["appmsg"]["finderFeed"]["objectNonceId"]
        senderUserName = xml_dict["msg"]["fromusername"]

        finderUserName = xml_dict["msg"]["appmsg"]["finderFeed"]["username"]
        finderNickName = xml_dict["msg"]["appmsg"]["finderFeed"]["nickname"]
        finderDescription = xml_dict["msg"]["appmsg"]["finderFeed"]["desc"]

        try:
            apiKey = config_loader.loadApiKey()
            res_data = requests.post(f"https://api.wxshares.com/api/qsy/sphzy?key={apiKey}&oid={objectId}&nid={objectNonceId}",timeout=5)
            res_json = res_data.json()
        except Exception as e:
            log.error(f"Exception during API call: {e}")
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
            return
        title = str(res_json['data']['title'])
        url = str(res_json['data']['url'])
        photo = str(res_json['data']['photo'])
        res_content = "标题：\n" + title + "\n\n" + "链接：\n" + url + "\n\n" + "图片：\n" + photo
        SendMsgNativeApi.send_text_message_base(wechatId
                                                , groupId if groupId else senderUserName
                                                , res_content
                                                , [senderUserName] if groupId else [])

        pass