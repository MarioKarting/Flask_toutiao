from . import db


class StatisticsArea:
    BEIJING = 1  # 北京
    SHANGHAI = 2  # 上海
    SHENZHEN = 3  # 深圳
    GUANGZHOU = 4  # 广州
    HANGZHOU = 5  # 杭州
    OTHER = 0  # 其他

    area_map = {
        BEIJING: '北京',
        SHANGHAI: '上海',
        SHENZHEN: '深圳',
        GUANGZHOU: '广州',
        HANGZHOU: '杭州',
        OTHER: '其他',
    }


class StatisticsType:
    # 网站统计
    DAY_ACTIVATE = 1  # 日活
    ACCESS = 2  # 访问
    ACCESS_IP = 3  # 访问IP
    NEW_USER = 4  # 新增用户
    SEARCH_USER = 5 # 搜索用户
    SEARCH = 6  # 搜索
    # 内容统计
    ARTICLE = 7  # 文章
    COMMENT = 8  # 评论
    READ = 9  # 阅读
    FORWARD = 10  # 转发

    type_map = {
        'day_activate': DAY_ACTIVATE,
        'access': ACCESS,
        'access_ip': ACCESS_IP,
        'new_user': NEW_USER,
        'search_user': SEARCH_USER,
        'search': SEARCH,
        'article': ARTICLE,
        'comment': COMMENT,
        'read': READ,
        'forward': FORWARD,
    }


class StatisticsBasic(db.Model):
    """
    基本统计
    """
    __tablename__ = 'statistics_basic'

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    year = db.Column(db.Integer, doc='年')
    month = db.Column(db.Integer, doc='月')
    day = db.Column(db.Integer, doc='日')
    hour = db.Column(db.Integer, doc='时')
    type = db.Column(db.Integer, doc='统计类型')
    count = db.Column(db.Integer, doc='数量')
    date_time = db.Column(db.DateTime, doc='跟年月日时匹配的时间')


class StatisticsSearchTotal(db.Model):
    """
    搜索统计-总数
    """
    __tablename__ = 'statistics_search_total'

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    keyword = db.Column(db.String, doc='搜索关键字')
    user_count = db.Column(db.Integer, doc='搜索用户数')
    count = db.Column(db.Integer, doc='搜索次数')


class StatisticsSearch(db.Model):
    """
    搜索统计
    """
    __tablename__ = 'statistics_search'

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    year = db.Column(db.Integer, doc='年')
    month = db.Column(db.Integer, doc='月')
    day = db.Column(db.Integer, doc='日')
    hour = db.Column(db.Integer, doc='时')

    keyword = db.Column(db.String, doc='搜索关键字')
    user_count = db.Column(db.Integer, doc='搜索用户数')
    count = db.Column(db.Integer, doc='搜索次数')
    date_time = db.Column(db.DateTime, doc='跟年月日时匹配的时间')


class StatisticsSalesTotal(db.Model):
    """
    销售额统计
    """
    __tablename__ = 'statistics_sales_total'

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    area = db.Column(db.Integer, doc='地区')
    money = db.Column(db.Integer, doc='金额(单位:分)')


class StatisticsReadSourceTotal(db.Model):
    """
    阅读来源统计-总数
    """
    __tablename__ = 'statistics_read_source_total'
    class SOURCE:
        RECOMMEND = 1  # 推荐
        CHANNEL = 2  # 频道
        RELATED_READING = 3  # 相关阅读
        APP_OUTSIDE = 4  # 应用外阅读
        OTHER = 0  # 其他
        source_map = {
            RECOMMEND: '推荐',
            CHANNEL: '频道',
            RELATED_READING: '相关阅读',
            APP_OUTSIDE: '应用外阅读',
            OTHER: '其他',
        }

    id = db.Column(db.Integer, primary_key=True, doc='主键id')
    source = db.Column(db.Integer, doc='阅读来源')
    count = db.Column(db.Integer, doc='阅读数量')
    count_20_down = db.Column(db.Integer, doc='完成度在20%以下的数量')
    count_20_80 = db.Column(db.Integer, doc='完成度在20%-80%的数量')
    count_80_up = db.Column(db.Integer, doc='完成度在80%以上的数量')


