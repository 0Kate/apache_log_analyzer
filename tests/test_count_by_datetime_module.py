import unittest

import apache_log_parser

from modules import CountByDatetimeModule


class TestCountByDatetimeModule(unittest.TestCase):
    TEST_LOG_FILE_PATH = 'tests/test.log'
    TEST_LOG_FORMAT = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
    
    def setUp(self):
        self.module = CountByDatetimeModule()
        self.parser = apache_log_parser.make_parser(self.__class__.TEST_LOG_FORMAT)

    def test_process(self):
        with open(self.__class__.TEST_LOG_FILE_PATH) as fp:
            for log_line in fp:
                log_data = self.parser(log_line)
                self.module.process(log_data)

        expect_result = {
            '09': 1,
            '10': 1,
            '12': 1,
        }

        self.assertEqual(dict(self.module.result), expect_result)
