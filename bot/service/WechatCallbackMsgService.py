import logging
import re

import xmltodict

from bot.config import config_loader
from bot.data import DbWaitVerifyFriend
from bot.service.WechatMsgHandle import WechatMsgHandle

log = logging.getLogger(__name__)


class WechatCallbackMsgService:

    def __init__(self):
        self.WechatMsgHandleHandle = WechatMsgHandle()
        self.callAdminUser = {}
        self.switPushType = {
            0: self.handleInterfaceAsyncResponse,
            1: self.handleSyncMessage,
            2: self.handleLoginEvent,
            3: self.handleLogoutEvent,
            4: self.handleSendMessageHook
        }

        self.switMsgType = {
            1: self.handle_text_message,
            3: self.handle_image_message,
            34: self.handle_voice_message,
            37: self.handle_friend_verify_message,
            42: self.handle_friend_recommend_message,
            47: self.handle_chat_emoji_message,
            48: self.handle_location_message,
            49: self.handle_xml_message,
            50: self.handle_video_call_message,
            51: self.handle_mobile_operation_message,
            10000: self.handle_system_notification_message,
            10002: self.handle_recall_message
        }
        pass

    def handle_wechat_message(self, response_data):
        pushType = response_data["pushType"]
        self.handleOriginMsg(pushType, response_data)

    def handleSyncMessage(self, response_data):
        # 1 同步消息
        # 消息体
        response_content_body = response_data["data"]
        syncFromMobile = response_content_body["syncFromMobile"]
        if syncFromMobile == 1:
            # 1. 如果是手机端发来的消息，直接返回
            log.warning(f"[handlePushMsg]sync message from mobile: {response_data}")
            return
        wechatId = response_content_body["to"]
        type = response_content_body["type"]
        self.handleByMsgType(type, wechatId, response_content_body)
        log.warning(f"[handlePushMsg]sync message not from mobile: {response_data}")

    def handle_text_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                            msgTime, adminMsgFlag, response_content_body):
        # 文本消息	1
        log.warning(f"[handle_text_message]text message: {response_content_body}")

        if response_content_body["isSender"] == 1:
            # 1. 如果是自己发的消息，直接返回 不处理
            target_user = response_content_body["talker"]
            return

        # 如果fromWechatId包含@chatroom，说明是群消息
        if "@chatroom" in fromWechatId:
            return

        # 如果是私聊消息，则开启一个对话线程，对话交互都会调用chatgpt的持续回复，持续回复的逻辑是，如果用户连续发消息，就连续回消息，
        # 最长消息间隔10分钟，超过10分钟，就开新的线程，最多保留最后20个消息
        self.WechatMsgHandleHandle.handle_user_message(wechatId, msgId, fromWechatId, msgContent, msgXml,
                                                       response_content_body)

        log.info(f"[handle_text_message]text message: {response_content_body}")
        pass

    def handle_image_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                             msgTime, adminMsgFlag, response_content_body):
        # 图片消息	3
        log.info(f"[handle_image_message]image message: {response_content_body}")
        pass

    def handle_voice_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                             msgTime, adminMsgFlag, response_content_body):
        # 语音消息	34
        log.info(f"[handle_voice_message]voice message: {response_content_body}")
        pass

    def handle_friend_verify_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                     msgTime, adminMsgFlag, response_content_body):
        # 好友验证消息	37
        log.info(f"[handle_friend_verify_message]friend verify message: {response_content_body}")
        # 提取 encryptusername 和 ticket
        encryptUserName = re.search(r'encryptusername="([^"]+)"', msgContent).group(1)
        ticket = re.search(r'ticket="([^"]+)"', msgContent).group(1)
        content = re.search(r'content="([^"]+)"', msgContent).group(1)
        wxid = re.search(r'fromusername="([^"]+)"', msgContent).group(1)

        if not config_loader.enableBotAccessAutoAddFriend():
            # 如果没开启自动通过好友验证则跳过
            return
        keyword = config_loader.autoAddFriendKeyword()
        # 验证消息中包含关键字或者没有设置关键字，才自动通过好友验证
        if not keyword or keyword in content:
            DbWaitVerifyFriend.insert_wait_verify_friend(wechatId, encryptUserName, ticket, content, wxid)
        pass

    def handle_friend_recommend_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                        msgTime, adminMsgFlag, response_content_body):
        # 好友推荐消息	42
        log.info(f"[handle_friend_recommend_message]friend recommend message: {response_content_body}")
        pass

    def handle_chat_emoji_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                  msgTime, adminMsgFlag, response_content_body):
        # 聊天表情	47
        log.info(f"[handle_chat_emoji_message]chat emoji message: {response_content_body}")
        pass

    def handle_location_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                msgTime, adminMsgFlag, response_content_body):
        # 位置消息	48
        log.info(f"[handle_location_message]location message: {response_content_body}")
        pass

    def handle_xml_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                           msgTime, adminMsgFlag, response_content_body):
        if "@chatroom" in fromWechatId:
            msgContent = msgContent.split(":\n")[1]
        xml_dict = xmltodict.parse(msgContent)
        xml_type = xml_dict["msg"]["appmsg"]["type"]
        if xml_type == "5":
            # 邀请入群消息
            log.info(f"[handle_xml_message]invite group message: {response_content_body}")
            return
        if xml_type == "51":
            # 视频号消息
            self.WechatMsgHandleHandle.handle_channel_message(wechatId, msgId, fromWechatId,
                                                              msgContent, msgXml, response_content_body, xml_dict)
            return
        # XML消息	49
        log.info(f"[handle_xml_message]xml message: " + str(response_content_body))
        pass

    def handle_video_call_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                  msgTime, adminMsgFlag, response_content_body):
        # 音视频通话	50
        log.info(f"[handle_video_call_message]video call message: {response_content_body}")
        pass

    def handle_mobile_operation_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                        msgTime, adminMsgFlag, response_content_body):
        # 手机端操作消息	51
        log.info(f"[handle_mobile_operation_message]mobile operation message: {response_content_body}")
        pass

    def handle_system_notification_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                                           msgTime, adminMsgFlag, response_content_body):
        # 系统通知	10000
        log.info(f"[handle_system_notification_message]system notification message: {response_content_body}")
        pass

    def handle_recall_message(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                              msgTime, adminMsgFlag, response_content_body):
        # 撤回消息	10002
        log.info(f"[handle_recall_message]recall message: {response_content_body}")
        pass

    def handle_other_msg_type(self, wechatId, msgId, fromWechatId, msgContent, msgXml,
                              msgTime, adminMsgFlag, response_content_body):
        # 其他消息类型
        log.info(
            f"[handle_other_msg_type]Unknown msgType: {response_content_body['type']},data:{response_content_body}")
        pass

    def handleLoginEvent(self, response_data):
        # 2 登录事件
        log.warning(f"[handlePushMsg]login event: {response_data}")
        pass

    def handleLogoutEvent(self, response_data):
        # 3 退出事件
        log.warning(f"[handlePushMsg]logout event: {response_data}")
        pass

    def handleSendMessageHook(self, response_data):
        # 4 主动发送消息HOOK
        log.warning(f"[handlePushMsg]send message hook: {response_data}")
        pass

    def handleInterfaceAsyncResponse(self, response_data):
        # 0 接口异步响应
        log.warning(f"[handlePushMsg]response: {response_data}")
        pass

    def handleOtherMes(self, response_data):
        # 其他消息类型
        log.warning(f"[handlePushMsg]Unknown pushType: {response_data['pushType']},data:{response_data}")
        pass

    def handleOriginMsg(self, case, response_data):
        self.switPushType.get(case, self.handleOtherMes)(response_data)

    def handleByMsgType(self, case, wechatId, response_content_body):
        msgId = response_content_body["msgSvrID"]
        fromWechatId = response_content_body["from"]
        msgContent = response_content_body["content"]
        msgXml = response_content_body["reversed1"]
        msgTime = response_content_body["createtime"]
        adminMsgFlag = self.WechatMsgHandleHandle.chekAdminMsgFlag(wechatId, response_content_body)
        self.switMsgType.get(case, self.handle_other_msg_type)(wechatId, msgId, fromWechatId, msgContent, msgXml,
                                                               msgTime, adminMsgFlag, response_content_body)
