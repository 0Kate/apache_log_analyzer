import unittest

from lib.apache_log_analyzer import ApacheLogAnalyzer
from modules import CountByDatetimeModule


class TestApacheLogAnalyzer(unittest.TestCase):
    """Test ApacheLogAnalyzer.
    """
    TEST_LOG_FILE_PATH = 'tests/test.log'
    TEST_LOG_FORMAT = \
        '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

    def setUp(self):
        self.analyzer = ApacheLogAnalyzer(
            [self.__class__.TEST_LOG_FILE_PATH],
            self.__class__.TEST_LOG_FORMAT
        )
        self.analyzer.add_module(CountByDatetimeModule)

    def test_process(self):
        results = self.analyzer.process()
        expected_result = (
            'CountByDatetimeModule:\n'
            '[Results]:\n'
            '09: 1\n'
            '10: 1\n'
            '12: 1\n'
            '[Errors]:\n'
        )
        self.assertEqual(results[0], expected_result)
