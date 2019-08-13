from flask import Blueprint
from flask_restful import Api

# from . import announcement, imtest
from utils.output import output_json

notice_bp = Blueprint('notice', __name__)
notice_api = Api(notice_bp, catch_all_404s=True)
notice_api.representation('application/json')(output_json)

# notice_api.add_resource(announcement.AnnouncementListResource, '/v1_0/announcements',
#                         endpoint='Announcements')
#
# notice_api.add_resource(announcement.AnnouncementResource, '/v1_0/announcements/<int(min=1):target>',
#                         endpoint='Announcement')
#
# notice_api.add_resource(imtest.IMTestResource, '/imtest/<string:event>',
#                         endpoint='IMTest')
