from flask import Blueprint
from flask_restful import Api

# from . import search, history
from utils.output import output_json

search_bp = Blueprint('search', __name__)
search_api = Api(search_bp, catch_all_404s=True)
search_api.representation('application/json')(output_json)

#
# search_api.add_resource(search.SearchResource, '/v1_0/search',
#                         endpoint='Search')
#
# search_api.add_resource(search.SuggestionResource, '/v1_0/suggestion',
#                         endpoint='Suggestion')
#
# search_api.add_resource(history.HistoryListResource, '/v1_0/search/histories',
#                         endpoint='Histories')
