import sys
import os
#BASE_DIR -->toutiao-backend
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#python解释器查找一个包的路径
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))
sys.path.insert(0, os.path.join(BASE_DIR))

from flask import jsonify

from . import create_app
from settings.default import DefaultConfig

#工厂函数，按需定制
app = create_app(DefaultConfig, enable_config_file=True)


@app.route('/')
def route_map():
    """
    主视图，返回所有视图网址
    """
    rules_iterator = app.url_map.iter_rules()
    return jsonify(
        {rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')})
