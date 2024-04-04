import os

from bot.infrastructure.wexin import WechatUtils


class ChannelNativeApi:
    """
    todo 视频号原生接口
    """
    pass


# 搜索视频号
def search_channel(wechat_id, keyword, lastBuffer=None):
    """
    todo 搜索视频号
    :param wechat_id: 微信id
    :param keyword: 关键字
    :return:
    """
    req = {
        "type": 10063,
        "keyword": keyword,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取作品列表
def get_channel_list(wechat_id, channel_user_id, lastBuffer=None):
    """
    获取作品列表
    :param wechat_id: 微信id
    :param channel_user_id: 视频号作者id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10038,
        "userName": channel_user_id,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata['data']


# 视频号作品解密
def decrypt_channel_video(wechat_id, inputFile, outputFile, decodeKey, encLength):
    """
    视频号作品解密
    :param wechat_id: 微信id
    :param inputFile: 已下载的加密视频绝对路径
    :param outputFile: 保存解密视频的绝对路径，需要包含文件名
    :param decodeKey: 获取作品列表接口会返回该字段
    :param encLength: 视频被加密的长度，下载视频时的header包含该字段
    :return:
    """
    req = {
        "type": 10060,
        "inputFile": inputFile,
        "outputFile": outputFile,
        "decodeKey": int(decodeKey),
        "encLength": int(encLength),
    }

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    # 删除inputFile
    os.remove(inputFile)
    return resdata


# 获取推荐内容
def get_recommend_channel(wechat_id, lastBuffer=None):
    """
    :param wechat_id: 微信id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10064,
        "longitude": "105.43",
        "latitude": "38.51",
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取作品弹幕
def get_channel_bullet(wechat_id, objectId, startTimestamp=None):
    """
    获取作品弹幕
    :param wechat_id: 微信id
    :param objectId: 视频号作者id
    :param startTimestamp: 开始获取弹幕的起始点，单位：毫秒
    :return:
    """
    req = {
        "type": 10065,
        "objectId": objectId,
    }
    if startTimestamp is not None:
        req["startTimestamp"] = startTimestamp
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取作品评论列表
def get_channel_comment_list(wechat_id, objectId, objectNonceId, rootCommentId=None, lastBuffer=None):
    """
    获取作品评论列表
    :param wechat_id: 微信id
    :param objectId: 视频号作者id
    :param objectNonceId: 作品nonceId
    :param rootCommentId: 评论id，如果设定了此参数，则会获取该评论的子评论列表
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10066,
        "objectId": objectId,
        "objectNonceId": objectNonceId,
        "h5AuthKey": "xxxxx",
    }

    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    if rootCommentId is not None:
        req["rootCommentId"] = rootCommentId

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取作品评论详情
def get_channel_comment_detail(wechat_id, channel_user_id, objectId, objectNonceId, lastBuffer=None,
                               sessionBuffer=None):
    """
    获取作品评论详情
    :param wechat_id: 微信id
    :param objectId: 视频号作者id
    :param objectNonceId: 作品nonceId
    :param commentId: 评论id
    :return:
    """
    req = {
        "type": 10067,
        "objectId": objectId,
        "objectNonceId": objectNonceId,
        "userName": channel_user_id,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer
    if sessionBuffer is not None:
        req["sessionBuffer"] = sessionBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata["data"]


# 获取我的关注列表
def get_my_follow_list(wechat_id, lastBuffer=None):
    """
    获取我的关注列表
    :param wechat_id: 微信id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10068,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取我的点赞列表
def get_my_like_list(wechat_id, lastBuffer=None):
    """
    获取我的点赞列表
    :param wechat_id: 微信id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10069,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取我的推荐列表
def get_my_recommend_list(wechat_id, lastBuffer=None):
    """
    获取我的推荐列表
    :param wechat_id: 微信id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10070,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取我的观看历史
def get_my_history_list(wechat_id, lastBuffer=None):
    """
    获取我的观看历史
    :param wechat_id: 微信id
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :return:
    """
    req = {
        "type": 10071,
    }
    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 关注/取关视频号
def follow_channel(wechat_id, channel_user_id, isFollow):
    """
    关注/取关视频号
    :param wechat_id: 微信id
    :param channel_user_id: 视频号作者id
    :param isFollow: True关注，False取关
    :return:
    """
    req = {
        "type": 10072,
        "userName": channel_user_id,
        "isFollow": isFollow,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 点赞/取消点赞内容
def like_channel(wechat_id, channel_user_id, objectId, objectNonceId, isLike, commentId=None):
    """
    点赞/取消点赞内容
    :param wechat_id: 微信id
    :param channel_user_id: 视频号作者id
    :param objectId: 作品id
    :param objectNonceId: 作品nonceId
    :param isLike: True点赞，False取消点赞
    :param commentId: 如果设定了此参数，则会对该评论进行操作
    :return:
    """
    req = {
        "type": 10073,
        "userName": channel_user_id,
        "objectId": objectId,
        "sessionBuffer": "...",
        "objectNonceId": objectNonceId,
        "isLike": isLike,
    }
    if commentId is not None:
        req["commentId"] = commentId

    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 推荐/取消推荐作品
def recommend_channel(wechat_id, objectId, objectNonceId, sessionBuffer, isFav):
    """
    推荐/取消推荐作品
    :param wechat_id: 微信id
    :param objectId: 作品id
    :param objectNonceId: 作品nonceId
    :param sessionBuffer: sessionBuffer
    :param isFav: 推荐/取消推荐
    :return:
    """
    req = {
        "type": 10074,
        "objectId": objectId,
        "sessionBuffer": sessionBuffer,
        "objectNonceId": objectNonceId,
        "isFav": isFav,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 获取作品推荐流
def get_channel_recommend_list(wechat_id, longitude, latitude, lastBuffer=None, sessionBuffer=None):
    """
    获取作品推荐流 另一种推荐接口，不区分标签。
    :param wechat_id: 微信id
    :param longitude: 经度
    :param latitude: 纬度
    :param lastBuffer: 指定结果的起始点，从返回的内容中获取
    :param sessionBuffer: sessionBuffer
    :return:
    """
    req = {
        "type": 10076,
        "longitude": longitude,
        "latitude": latitude,
    }

    if lastBuffer is not None:
        req["lastBuffer"] = lastBuffer
    if sessionBuffer is not None:
        req["sessionBuffer"] = sessionBuffer
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 发布/回复评论
def publish_channel_comment(wechat_id, objectId, objectNonceId, content, sessionBuffer, replyCommentId=None):
    """
    发布/回复评论
    :param wechat_id: 微信id
    :param objectId: 作品id
    :param objectNonceId: 作品nonceId
    :param content: 评论内容
    :param sessionBuffer: sessionBuffer
    :param replyCommentId: 如果设定了此参数，则会对该评论进行回复
    :return:
    """
    req = {
        "type": 10077,
        "objectId": objectId,
        "objectNonceId": objectNonceId,
        "sessionBuffer": sessionBuffer,
        "content": content,
    }
    if replyCommentId is not None:
        req["replyCommentId"] = replyCommentId
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata


# 删除评论
def delete_channel_comment(wechat_id, objectId, objectNonceId, commentId, sessionBuffer):
    """
    删除评论
    :param wechat_id: 微信id
    :param objectId: 作品id
    :param objectNonceId: 作品nonceId
    :param commentId: 评论id
    :param sessionBuffer: sessionBuffer
    :return:
    """
    req = {
        "type": 10078,
        "objectId": objectId,
        "objectNonceId": objectNonceId,
        "sessionBuffer": sessionBuffer,
        "commentId": commentId,
    }
    resdata = WechatUtils._post_wx_request(wechat_id, req)
    return resdata
