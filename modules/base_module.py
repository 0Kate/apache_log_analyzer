from abc import abstractmethod, ABCMeta

class BaseModule(object):
    __metaclass__  = ABCMeta

    @abstractmethod
    def process(self, log_data: dict):
        raise NotImplementedError()

    @abstractmethod
    def error_lines(self, line_num: int, exc: Exception):
        raise NotImplementedError()

    @abstractmethod
    def output(self):
        raise NotImplementedError()
