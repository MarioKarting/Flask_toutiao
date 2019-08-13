from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm
import random

from .session import RoutingSession


class RoutingSQLAlchemy(SQLAlchemy):
    """
    自定补充数据库路由的SQLAlchemy
    """
    master_binds = []
    slave_binds = []
    default_bind = ''

    def create_session(self, options):
        return orm.sessionmaker(class_=RoutingSession, db=self, **options)

    def get_binds(self, app=None):
        app = self.get_app()
        config_binds = app.config.get('SQLALCHEMY_BINDS')
        if not config_binds:
            raise RuntimeError('Missing SQLALCHEMY_BINDS config.')

        self.master_binds = list(config_binds.get('masters') or ())
        self.slave_binds = list(config_binds.get('slaves') or ())
        self.default_bind = config_binds.get('default')

        binds = self.master_binds + self.slave_binds
        for bind in binds:
            self.get_engine(app, bind)

        return {}

    def get_bind_for_write(self):
        """
        获取写使用的数据库
        """
        return random.choice(self.master_binds)

    def get_bind_for_read(self):
        """
        获取读使用的数据库
        """
        return random.choice(self.slave_binds)
