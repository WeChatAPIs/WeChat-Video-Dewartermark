import asyncio
import logging
import random
import threading
import time

from bot.config import config_loader
from bot.data import DbWaitVerifyFriend
from bot.infrastructure.wexin import WechatUtils, MsgProcessorNativeApi, ContactNativeApi
from bot.service.WechatCallbackMsgService import WechatCallbackMsgService

log = logging.getLogger(__name__)


class RequestHandler:
    def __init__(self):
        self.wechatService = WechatCallbackMsgService()
        if config_loader.enableBotAccessAutoAddFriend():
            # 处理好友通过消息
            try:
                user_data = WechatUtils._post_wx_request("-", {"type": 28})
                userName = user_data['data']['userName']
            except Exception as e:
                log.error(f"获取微信用户信息失败,请登录微信号后重试: {e}")
                raise Exception(f"获取微信用户信息失败,请登录微信号后重试")

            thread_verify_friend = threading.Thread(target=self.handle_verify_friend, args=(userName,))
            thread_verify_friend.start()

    def handle_weixin_callback(self, user_input):
        self.wechatService.handle_wechat_message(user_input)

    def poll_weixin_api(self, wechat_pull_url):
        # 循环调用微信API,获取消息
        while config_loader.App_Run_Status:
            try:
                response_data = WechatUtils.pull_message(wechat_pull_url)
                if response_data is not None:
                    # self.wechatService.handle_wechat_message(response_data)
                    asyncio.run(self.wechatService.handle_wechat_message(response_data))
            except Exception as e:
                log.error(f"Exception during API call: {e}")
            time.sleep(5)

    def init_weixin_callbackUrl(self, callbackUrl):
        # 给所有微信设置回调地址
        MsgProcessorNativeApi.add_http_processor_forAll(callbackUrl)

    def handle_verify_friend(self, userName):
        log.info("开启自动通过好友验证")
        while True:
            time.sleep(random.randint(10, 15))
            # 通过好友验证
            data = DbWaitVerifyFriend.select_wait_verify_friend([userName])
            # log.info("handle verify friend,size:" + str(len(data)))
            for item in data:
                id, wechatId, encryptUserName, ticket = item[0], item[1], item[2], item[3]
                ContactNativeApi.accept_friend(wechatId, encryptUserName, ticket)
                DbWaitVerifyFriend.delete_wait_verify_friend(id)
                log.info(f"通过好友验证 {wechatId} {id}")
