# 不能用current_app,current_app只能取数据，不能定义数据

from flask import request, g

from utils.jwt_util import verify_jwt


def jwt_authentication():
    # 从请求头中取出token
    g.user_id = None
    g.use_refersh_token = False
    token = request.headers.get("Authorization")
    if token is not None and token.startswith('Bearer '):
        # 验证token
        # Bearer
        token = token[7:]
        payload = verify_jwt(token)
        if payload is not None:
            g.user_id = payload.get('user_id')
            g.use_refersh_token = payload.get('is_refresh', False)
