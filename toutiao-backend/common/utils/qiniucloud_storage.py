from qiniu import Auth, put_file, etag, put_data
import qiniu.config
from flask import current_app


def upload_image(file_data):
    '''
    七牛云耶耶耶
    :param file_data: 二进制文件哟
    :return: 返回的是名字哟
    '''
    # 需要填写你的Access Key(访问密钥)和Secret Key（加密密钥）
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建一个鉴权对象，鉴权是指验证用户是否拥有访问系统的权利
    q = Auth(access_key, secret_key)
    # 要上传到七牛云的存储空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']
    #上传后保存的文件名自己制定
    key = None
    #自动生成上传Token，可以指定对象过期时间哟
    token = q.upload_token(bucket_name, key, 3600000)
    ret, info = put_data(token, key, file_data)
    file_name = ret['key']
    return file_name