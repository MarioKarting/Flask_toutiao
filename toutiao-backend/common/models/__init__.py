# from flask_sqlalchemy import SQLAlchemy
from .db_routing.routing_sqlalchemy import RoutingSQLAlchemy


db = RoutingSQLAlchemy()
