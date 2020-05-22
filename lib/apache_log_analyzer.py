from collections import defaultdict
from datetime import datetime
from pprint import pprint
from typing import List

import apache_log_parser


class ApacheLogAnalyzer(object):
    """Analyzer that analyze log of apache.

    Attributes:
        target_files (List[str]): target files to analyze
        log_format (str): log format to analyze
        range_min (str): minimum datetime of target log
        range_max (str): maximum datetime of target log
        parser (ApacheLogParser): parser that parse logs
        modules (List[BaseModules]): list of applyed modules
    """
    RANGE_DATESTR_FORMAT = '%Y/%m/%d'

    def __init__(
            self,
            target_files: List[str],
            log_format: str,
            range_min='',
            range_max=''):
        """Initialize ApacheLogAnalyzer.

        Args:
            target_files (List[str]): target files to analyze
            log_format (str): log format to analyze
            range_min (str): minimum datetime of target log
            range_max (str): maximum datetime of target log
        """
        self.target_files = target_files
        self.log_format = log_format
        self.range_min = range_min
        self.range_max = range_max
        self.parser = apache_log_parser.make_parser(log_format)
        self.modules = []

    def add_module(self, module):
        """Create module instance and add to modules list.

        Args:
            module (BaseModule): module to apply
        """
        self.modules.append(module())

    def process(self) -> List[str]:
        """Start analyze.

        Returns:
            List[str]: list of string that processed results
        """
        if self.range_min:
            self.range_min = \
                self._parse_range_datestr(self.range_min)

        if self.range_max:
            self.range_max = \
                self._parse_range_datestr(self.range_max)

        for target_file in self.target_files:
            self._process_line_by_line(target_file)

        return [module.output() for module in self.modules]

    def _parse_range_datestr(self, range_datestr):
        """Parse range date string.

        Args:
            range_datestr (str): string of datetime

        Returns:
            datetime.datetime: datetime object of parsed from range_datetime
        """
        return datetime.strptime(
            range_datestr,
            self.__class__.RANGE_DATESTR_FORMAT
        )

    def _process_line_by_line(self, target_file: str):
        """Get file name and process line by line.

        Args:
            target_file (str): target file name to process by each applyed modules
        """
        with open(target_file) as fp:
            line_num = 0
            for log_line in fp:
                line_num += 1
                parsed_data = self.parser(log_line.strip('\n'))

                if 'time_received_datetimeobj' in parsed_data:
                    received_datetimeobj = parsed_data['time_received_datetimeobj']

                    if self.range_min and received_datetimeobj < self.range_min:
                        continue

                    if self.range_max and self.range_max < received_datetimeobj:
                        continue

                for module in self.modules:
                    try:
                        module.process(parsed_data)
                    except Exception as ex:
                        module.error_line(line_num, ex)
