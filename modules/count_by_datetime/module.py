from collections import defaultdict

from ..base_module import BaseModule


class CountByDatetimeModule(BaseModule):
    def __init__(self, config={}):
        self.config = config
        self.result = defaultdict(int)

    def process(self, log_data: dict):
        received_datetimeobj = log_data['time_received_datetimeobj']

        datetime_str = \
            received_datetimeobj.strftime('%Y/%m/%d %H')
        self.result[datetime_str] += 1


