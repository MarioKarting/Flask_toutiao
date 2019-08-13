from flask import current_app, jsonify


def handle_redis_error(e):
    """
    处理redis异常
    **********已废弃***********
    """
    current_app.logger.error('[Redis] {}'.format(e))
    return jsonify(message='Unavailable service.'), 507


def handler_mysql_error(e):
    """
    处理mysql异常
    **********已废弃***********
    """
    current_app.logger.error('[MySQL] {}'.format(e))
    return jsonify(message='Unavailable service.'), 507


# *******已废弃*******
# 定义错误的响应信息
error_messages = {
    'RedisError': {
        'message': 'Unavailable service.',
        'status': 507,
    },
    'SQLAlchemyError': {
        'message': 'Unavailable service',
        'status': 507
    }
}
