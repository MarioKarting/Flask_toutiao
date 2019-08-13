from apscheduler.executors.pool import ThreadPoolExecutor
from flask import Flask
from redis.exceptions import RedisError
from sqlalchemy.exc import SQLAlchemyError
import grpc
from elasticsearch5 import Elasticsearch
from apscheduler.schedulers.background import BackgroundScheduler

# import socketio


def create_flask_app(config, enable_config_file=False):
    """
    创建Flask应用
    :param confi g: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(config)
    #标志位，是否加载系统环境
    if enable_config_file:
        from utils import constants
        app.config.from_envvar(constants.GLOBAL_SETTING_ENV_NAME, silent=True)

    return app


def create_app(config, enable_config_file=False):
    """
    创建应用
    :param config: 配置信息对象
    :param enable_config_file: 是否允许运行环境中的配置文件覆盖已加载的配置信息
    :return: 应用
    """
    app = create_flask_app(config, enable_config_file)

    # 创建Snowflake ID worker
    from utils.snowflake.id_worker import IdWorker
    app.id_worker = IdWorker(app.config['DATACENTER_ID'],
                             app.config['WORKER_ID'],
                             app.config['SEQUENCE'])

    # 限流器
    from utils.limiter import limiter as lmt
    lmt.init_app(app)

    # 配置日志
    from utils.logging import create_logger
    create_logger(app)

    # 注册url转换器
    from utils.converters import register_converters
    register_converters(app)

    from redis.sentinel import Sentinel
    _sentinel = Sentinel(app.config['REDIS_SENTINELS'])
    app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
    app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])

    from rediscluster import StrictRedisCluster
    app.redis_cluster = StrictRedisCluster(startup_nodes=app.config['REDIS_CLUSTER'])

    # rpc
    app.rpc_reco = grpc.insecure_channel(app.config['RPC'].RECOMMEND)

    # Elasticsearch
    app.es = Elasticsearch(
        app.config['ES'],
        # sniff before doing anything
        sniff_on_start=True,
        # refresh nodes after a node fails to respond
        sniff_on_connection_fail=True,
        # and also every 60 seconds
        sniffer_timeout=60
    )

    # socket.io
    # app.sio = socketio.KombuManager(app.config['RABBITMQ'], write_only=True)

    # MySQL数据库连接初始化
    from models import db

    db.init_app(app)

    # 添加请求钩子
    from utils.middlewares import jwt_authentication
    app.before_request(jwt_authentication)

    # 注册用户模块蓝图
    from .resources.user import user_bp
    app.register_blueprint(user_bp)

    # 注册新闻模块蓝图
    from .resources.news import news_bp
    app.register_blueprint(news_bp)

    # 注册通知模块
    from .resources.notice import notice_bp
    app.register_blueprint(notice_bp)

    # 搜索
    from .resources.search import search_bp
    app.register_blueprint(search_bp)

    # 定义apscheduler的调度器对象
    # 保存到flask的app对象，方便在视图中使用调度器添加新的定时任务
    executors = {
        'default': ThreadPoolExecutor(20),
    }
    app.scheduler = BackgroundScheduler(executors=executors)

    # 由scheduler管理的定时任务 两种：
    # 一种是一开始就明确确定的 ，比如 修正redis的统计数据
    # 在此处定义 add_job
    # app.scheduler.add_job()

    # 添加定时修正统计数据的定时任务
    from .schedulers.statistic import fix_statistics
    # 每天的凌晨3点执行
    # 通过args 可以在调度器执行定时任务方法的时候，传递给定时任务方法参数
    # app.scheduler.add_job(fix_statistics, 'cron', hour=3, args=[app])

    # 为了测试方便，需要立即执行
    app.scheduler.add_job(fix_statistics, 'date', args=[app])

    # 另一种 是在flask运行期间，由视图函数产生的，动态添加的新定时任务
    # 在视图函数中 调用 current_app.scheduler.add_job来添加

    app.scheduler.start()  # 非阻塞，不会阻塞住flask程序的执行，会在后台单独创建进程或线程进行计时

    return app


