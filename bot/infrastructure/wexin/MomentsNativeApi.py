import time

from bot.config import config_loader
from bot.infrastructure.wexin import WechatUtils
from bot.utils import IdUtils, FileUtils


class MomentsNativeApi:
    """
    todo 朋友圈原生接口
    """
    pass


# 获取朋友圈信息
def get_moments(wechat_id, startId=None):
    """
    获取朋友圈信息
    :param wechat_id: 微信id
    :param startId: 朋友圈id，指定从何处开始获取
    :return:
    """
    req = {
        "type": 18,
    }
    if startId is not None:
        req["startObjectId"] = startId
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取指定用户的朋友圈信息。
def get_moments_by_user(wechat_id, user_id, startId=None):
    """
    获取指定用户的朋友圈信息
    :param wechat_id: 微信id
    :param user_id: 用户id
    :param startId: 朋友圈id，指定从何处开始获取
    :return:
    """
    req = {
        "type": 20,
        "userName": user_id
    }
    if startId is not None:
        req["startObjectId"] = startId
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 点赞朋友圈
def like_moments(wechat_id, user_id, moment_id):
    """
    点赞朋友圈
    :param wechat_id: 微信id
    :param user_id: 发布者wxid
    :param moment_id: 朋友圈id
    :return:
    """
    req = {
        "type": 10016,
        "userName": user_id,
        "objectId": moment_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 评论朋友圈
def comment_moments(wechat_id, user_id, moment_id, content):
    """
    评论朋友圈
    :param wechat_id: 微信id
    :param user_id: 发布者wxid
    :param moment_id: 朋友圈id
    :param content: 评论内容
    :return:
    """
    req = {
        "type": 10017,
        "userName": user_id,
        "objectId": moment_id,
        "commentContent": content,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 回复朋友圈评论
def reply_comment_moments(wechat_id, user_id, reply_user_id, moment_id, comment_id, content):
    """
    回复朋友圈评论
    :param wechat_id: 微信id
    :param user_id: 发布者wxid
    :param reply_user_id: 回复对象wxid
    :param moment_id: 朋友圈id
    :param comment_id: 评论id
    :param content: 评论内容
    :return:
    """
    req = {
        "type": 10018,
        "userName": user_id,
        "replyUserName": reply_user_id,
        "objectId": moment_id,
        "replyCommentId": comment_id,
        "commentContent": content
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 取消点赞朋友圈
def unlike_moments(wechat_id, moment_id):
    """
    取消点赞朋友圈
    :param wechat_id: 微信id
    :param moment_id: 朋友圈id
    :return:
    """
    req = {
        "type": 10019,
        "objectId": moment_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 删除朋友圈评论
def delete_comment_moments(wechat_id, moment_id, comment_id):
    """
    删除朋友圈评论
    :param wechat_id: 微信id
    :param moment_id: 朋友圈id
    :param comment_id: 评论id
    :return:
    """
    req = {
        "type": 10020,
        "objectId": moment_id,
        "commentId": comment_id
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 删除朋友圈
def delete_moments(wechat_id, moment_id):
    """
    删除已发布的朋友圈
    :param wechat_id: 微信id
    :param moment_id: 朋友圈id
    :return:
    """
    req = {
        "type": 10021,
        "objectId": moment_id,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 上传朋友圈图片
def upload_moments_image(wechat_id, filePath):
    """
    上传朋友圈图片
    :param wechat_id: 微信id
    :param filePath: 文件路径 本地文件或者http开头的url
    :return:
    """
    filePath, md5 = WechatUtils.getFilePathAndMd5(filePath)
    req = {
        "type": 5,
        "filePath": filePath
    }
    return WechatUtils._post_wx_request(wechat_id, req)


# 获取企业用户朋友圈信息
def get_enterprise_moments(wechat_id, openIMUserName, startId=None):
    """
    获取企业用户朋友圈信息
    :param wechat_id: 微信id
    :param openIMUserName: 企业用户wxid，可以从数据库中读取
    :param startId: 朋友圈id，指定从何处开始获取
    :return:
    """
    req = {
        "type": 80,
        "openIMUserName": openIMUserName,
    }
    if startId is not None:
        req["startObjectId"] = startId
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata
