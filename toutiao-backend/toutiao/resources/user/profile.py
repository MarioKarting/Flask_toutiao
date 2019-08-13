from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import g, current_app

from utils.decorators import login_required
from utils import parser
from utils.qiniucloud_storage import upload_image
from models.user import User
from models import db
from cache import user as cache_user  # 起别名
from cache import statistic as cache_statistic

# /users/123
# /users/<int(min=1):user_id>
class UserResource(Resource):
    """
    用户个人信息
    """
    def get(self, user_id):

        # 检验参数
        cache_tool = cache_user.UserProfileCache(user_id)
        if not cache_tool.exists():
            # 用户不存在
            return {'message': 'User does not exists.'}, 404
        else:
            # {
            # 	"message": "OK",
            # 	"data": {
            # 		"user_id": xx,
            # 		"name": xx,
            # 		"photo":xx,
            # 		"intro": xx,
            # 		"certi": xx,
            # 		"artile_count": xx,
            # 		"follows_count": xx,
            # 		"fans_count": xx,
            # 		"liking_count": xx
            # 	}
            # }

            # 查询用户数据
            user_dict = cache_tool.get()
            user_dict['user_id'] = user_id
            user_dict['photo'] = current_app.config['QINIU_DOMAIN'] + user_dict['photo']

            del user_dict['mobile']

            user_dict['article_count'] =cache_statistic.UserArtuclesCountStorage.get(user_id)
            user_dict['follows_count'] =cache_statistic.UserFollowsCountStorage.get(user_id)
            user_dict['fans_count'] =cache_statistic.UserFansCountStorage.get(user_id)
            user_dict['liking_count'] =cache_statistic.UserLikingCountStorage.get(user_id)

            return user_dict



class PhotoResource(Resource):
    """
    用户头像
    """
    # 装饰器方法
    method_decorators = [login_required]

    def patch(self):
        """
        修改
        :return:
        """
        # 接收参数 检验参数
        rp = RequestParser()
        # 接收表单数据photo，用type进行图片校验，是否是图片，必须传，location 描述参数应该在请求数据中出现的位置
        # location='files' 请求体中以文件位置出现
        rp.add_argument('photo', type=parser.check_image, required=True, location='files')  # request.files.get('photo')
        # 使用parse_args()方法启动检验处理
        # 检验之后从检验结果中获取参数时可按照字典操作或对象属性操作
        req = rp.parse_args()
        # 取出图片对象
        image_file = req.photo
        # 读取图片的二进制流
        image_data = image_file.read()

        # 业务处理
        #  上传到七牛，返回存储在七牛云的中的文件名
        file_name = upload_image(image_data)

        #  保存数据库
        # try:
        # user1.profile_photo =
        # db.session.add(user1)
        # db.session.commit()

        User.query.filter(User.id == g.user_id).update({'profile_photo': file_name})
        db.session.commit()
        # except Exception:
        #     db.session.rollback()
        #     return {}

        # 返回    QINIU_DOMAIN = 'http://puvqndbgh.bkt.clouddn.com/'
        photo_url = current_app.config['QINIU_DOMAIN'] + file_name
        return {'photo_url': photo_url}, 201

