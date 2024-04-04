import json
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
            url = "https://api-cn.lucktoyou.space/v1/chat/completions"
            payload = json.dumps({
                "messages": [
                    {
                        "role": "url",
                        "content": link[0]
                    }
                ],
                "model": "dsp"
            })
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {apiKey}',
            }
            response_content_body = requests.request("POST", url, headers=headers, data=payload)

            res_data = response_content_body.json()
        except Exception as e:
            log.error(f"Exception during API call: {e}")
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
            return
        if res_data['code'] != "200":
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
        title = res_data['data']['data']['title']
        url = res_data['data']['data']['url']
        photo = res_data['data']['data']['photo']
        picsList = []
        if 'pics' in res_data['data']['data']:
            picsList = res_data['data']['data']['pics']

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
            url = "https://api-cn.lucktoyou.space/v1/chat/completions"
            payload = json.dumps({
                "messages": [
                    {
                        "role": "oid",
                        "content": objectId
                    },
                    {
                        "role": "nid",
                        "content": objectNonceId
                    }
                ],
                "model": "sph"
            })
            headers = {
                'content-type': 'application/json',
                'Authorization': f'Bearer {apiKey}',
            }
            res_data = requests.request("POST", url, headers=headers, data=payload)

            res_json = res_data.json()
        except Exception as e:
            log.error(f"Exception during API call: {e}")
            SendMsgNativeApi.send_text_message_base(wechatId, fromWechatId
                                                    , "很抱歉解析失败了，可能是链接已经过期了", [])
            return
        title = str(res_json['data']['data']['title'])
        url = str(res_json['data']['data']['url'])
        photo = str(res_json['data']['data']['photo'])
        res_content = "标题：\n" + title + "\n\n" + "链接：\n" + url + "\n\n" + "图片：\n" + photo
        SendMsgNativeApi.send_text_message_base(wechatId
                                                , groupId if groupId else senderUserName
                                                , res_content
                                                , [senderUserName] if groupId else [])

        pass
