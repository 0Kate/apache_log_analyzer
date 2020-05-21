from collections import defaultdict
from datetime import datetime
from typing import List

import apache_log_parser


class ApacheLogAnalyzer(object):
    RANGE_DATESTR_FORMAT = '%Y/%m/%d'

    def __init__(
            self,
            target_files: List[str],
            log_format: str,
            range_min='',
            range_max=''):
        self.target_files = target_files
        self.log_format = log_format
        self.range_min = range_min
        self.range_max = range_max
        self.parser = apache_log_parser.make_parser(log_format)
        self.modules = []

    def add_module(self, module, config={}):
        self.modules.append(module(config=config))

    def process(self) -> List[defaultdict]:
        if self.range_min:
            self.range_min = \
                self._parse_range_datestr(self.range_min)

        if self.range_max:
            self.range_max = \
                self._parse_range_datestr(self.range_max)

        for target_file in self.target_files:
            self._process_line_by_line(target_file)

        return [module.result for module in self.modules]

    def _parse_range_datestr(self, range_datestr):
        return datetime.strptime(
            range_datestr,
            self.__class__.RANGE_DATESTR_FORMAT
        )

    def _process_line_by_line(self, target_file):
        with open(target_file) as fp:
            for log_line in fp:
                parsed_data = self.parser(log_line.strip('\n'))
                received_datetimeobj = parsed_data['time_received_datetimeobj']

                if self.range_min and received_datetimeobj < self.range_min:
                    return

                if self.range_max and self.range_max < received_datetimeobj:
                    return

                for module in self.modules:
                    module.process(parsed_data)
