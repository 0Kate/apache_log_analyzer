from collections import defaultdict

from ..base_module import BaseModule


class CountByDatetimeModule(BaseModule):
    """Count by datetime.

    Attributes:
        result (defaultdict): count results
        error_lines (dict): log lines that error occured

    """

    def __init__(self):
        """Initialize CountByDatetimeModule.
        """
        self.result = defaultdict(int)
        self.error_lines = {}

    def process(self, log_data: dict):
        """Increment count by datetime.

        Args:
            log_data (dict): parsed log data
        """
        received_datetimeobj = log_data['time_received_datetimeobj']

        datetime_str = \
            received_datetimeobj.strftime('%H')
        self.result[datetime_str] += 1

    def error_line(self, line_num: int, exc: Exception):
        """Add line that error occured.

        Args:
            line_num (int): number of line
            exc (Exception): content of exception
        """
        self.error_lines[line_num] = f'{exc.__class__.__name__} {str(exc)}'

    def output(self):
        """Return string to output.

        Retutns:
            str: string to output.
        """
        return (
            f'{self.__class__.__name__}:\n'
            '[Results]:\n'
            f'{self._output_results()}\n'
            '[Errors]:\n'
            f'{self._output_errors()}'
        )

    def _output_results(self):
        result_strs = []
        for key, value in self.result.items():
            result_strs.append(f'{key}: {value}')

        return '\n'.join(result_strs)

    def _output_errors(self):
        error_strs = []
        for key, value in self.error_lines.items():
            error_strs.append(f'{key}: {value}')

        return '\n'.join(error_strs)
