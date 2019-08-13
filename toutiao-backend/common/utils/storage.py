from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config
from qiniu.compat import is_py2, is_py3
from flask import current_app


def upload_image(file_data):
    """
    上传图片到七牛
    :param file_data: bytes 文件
    :return: file_name
    """
    # 需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']

    # 上传到七牛后保存的文件名
    # key = 'my-python-七牛.png'
    key = None

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, expires=1800)

    # # 要上传文件的本地路径
    # localfile = '/Users/jemy/Documents/qiniu.png'

    # ret, info = put_file(token, key, localfile)
    ret, info = put_data(token, key, file_data)

    # print(ret)
    # print(info)

    # if is_py2:
    #     assert ret['key'].encode('utf-8') == key
    # elif is_py3:
    #     assert ret['key'] == key
    #
    # assert ret['hash'] == etag(localfile)
    return ret['key']
