import os

from bot.config import config_loader
from bot.infrastructure.wexin import WechatUtils


class CdnNativeApi:
    """
    CDN原生接口
    """
    pass

def upload_to_cdn(wechatId: object, file_path: object, type: object = 5) -> object:
    """
    上传文件到微信CDN
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    # 如果是http开头的，下载到本地，然后上传
    # 如果是本地文件，直接上传
    local_file_path, md5 = WechatUtils.getFilePathAndMd5(file_path)
    resdata = WechatUtils._post_wx_request(wechatId, {
        "type": 7,
        "filePath": local_file_path,
        "aeskey": md5,
        "fileType": type,
    })
    return resdata["data"]["fileId"]


def download_from_cdn(wechatId: str, file_id: str, aeskey: str, fileType: int, path: str) -> object:
    """

    从微信CDN下载文件
    :param wechatId:
    :param file_id: 文件ID
    :param aeskey: aeskey
    :param fileType: 图片2、视频4、文件5、语音15
    :return: 文件路径

    """
    req = {
        "type": 66,
        "fileid": file_id,
        "aeskey": aeskey,
        "fileType": fileType,
        "savePath": path
    }
    resdata = WechatUtils._post_wx_request(wechatId, req)
    return path if resdata["status"] == 0 else None


def download_img_from_cdn(wechatId: str, file_id: str, aeskey: str) -> object:
    """
    从微信CDN下载图片
    :param wechatId:
    :param file_id: 文件ID
    :return: 文件路径
    """
    filePath = config_loader.DOWN_FILE_PATH + file_id + ".png"

    return download_from_cdn(wechatId, file_id, aeskey, 2, filePath)


def upload_img_to_cdn(wechatId: object, file_path: object) -> object:
    """
    上传图片到微信CDN
    :param wechatId:
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    return upload_to_cdn(wechatId, file_path, 2)


def upload_audio_to_cdn(wechatId: object, file_path: object) -> object:
    """
    上传语音
    :param wechatId:
    :param file_path: 文件路径 本地文件或者http开头的url
    :return: fileId
    """
    return upload_to_cdn(wechatId, file_path, 15)
