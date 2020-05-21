import unittest

from lib.apache_log_analyzer import ApacheLogAnalyzer


class TestApacheLogAnalyzer(unittest.TestCase):
    TEST_LOG_FILE_PATH = 'tests/test.log'
    TEST_LOG_FORMAT = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'

    def setUp(self):
        self.analyzer = ApacheLogAnalyzer(
            self.__class__.TEST_LOG_FILE_PATH,
            self.__class__.TEST_LOG_FORMAT
        )
