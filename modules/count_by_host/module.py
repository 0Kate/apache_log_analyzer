from collections import defaultdict

from ..base_module import BaseModule


class CountByHostModule(BaseModule):
    def __init__(self, config: dict = {}):
        self.config = config
        self.result = defaultdict(int)

    def process(self, log_data: dict):
        remote_host = log_data['remote_host']
        self.result[remote_host] += 1
