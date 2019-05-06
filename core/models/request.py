from datetime import datetime
from core.utilities import utils


class Request(object):
    def __init__(self, request: dict):
        self.id: int = request.get('id')
        self.start_ts: datetime = utils.parse_datetime(request.get('startTs'))
        self.end_ts: datetime = utils.parse_datetime(request.get('endTs'))
        self.offset: int = request.get('offset') or 0
        self.limit: int = request.get('limit') or 10
