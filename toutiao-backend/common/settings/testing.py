from .default import DefaultConfig


class TestingConfig(DefaultConfig):
    """
    单元测试配置
    """
    TESTING = True
