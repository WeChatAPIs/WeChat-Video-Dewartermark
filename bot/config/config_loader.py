import os

from dotenv import load_dotenv

load_dotenv()


def loadWechatAPIConfig():
    bot_api_url = os.environ.get('BOT_API_URL', '')
    if not bot_api_url:
        raise Exception("BOT_API_URL 需要配置在 .env 文件中")
    return bot_api_url

def loadApiKey():
    bot_api_url = os.environ.get('BOT_REMOVE_WARTERMARK_API_KEY', '')
    if not bot_api_url:
        raise Exception("BOT_REMOVE_WARTERMARK_API_KEY 需要配置在 .env 文件中")
    return bot_api_url


def enableBotAccessAutoAddFriend():
    enable = os.environ.get('BOT_ACCESS_AUTO_ADD_FRIEND', False)
    return enable


def autoAddFriendKeyword():
    enable = os.environ.get('BOT_ACCESS_AUTO_ADD_FRIEND_KEYWORD', '')
    return enable


def getAdminUserName():
    enable = os.environ.get('BOT_ADMIN_USER', '')
    return enable
