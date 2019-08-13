from flask_sqlalchemy import SignallingSession, get_state


class RoutingSession(SignallingSession):
    """
    补充路由的session
    """
    def __init__(self, db, bind_name=None, autocommit=False, autoflush=True, **options):
        self._name = bind_name
        SignallingSession.__init__(self, db, autocommit=autocommit, autoflush=autoflush, **options)

    def get_bind(self, mapper=None, clause=None):
        """
        获取数据库绑定
        """
        # For test
        print('Calling get_bind: _name={}'.format(self._name))

        state = get_state(self.app)

        if self._name:
            # 指定
            print('Using DB bind: _name={}'.format(self._name))
            return state.db.get_engine(self.app, bind=self._name)
        else:
            # 默认数据库
            print('Using default DB bind: _name={}'.format(state.db.default_bind))
            return state.db.get_engine(self.app, bind=state.db.default_bind)

    def set_to_write(self):
        """
        设置用写数据库
        """
        state = get_state(self.app)

        self._name = state.db.get_bind_for_write()

    def set_to_read(self):
        """
        设置用读数据库
        """
        state = get_state(self.app)

        self._name = state.db.get_bind_for_read()
