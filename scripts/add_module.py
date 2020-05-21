import re
import sys
import os


INIT_CODE_TEMPLATE = \
'''from .module import %s
'''


MODULE_CODE_TEMPLATE = \
'''from ..base_module import BaseModule


class %s(BaseModule):
    def __init__(self, config: dict = {}):
        self.config = config
        self.result = {}

    def process(self, log_data):
        ...
'''


def to_camel_case(snake_case_str: str) -> str:
    return re.sub('(?:^|_)(.)', lambda x: x.group(1).upper(), snake_case_str)


def to_snake_case(camel_case_str: str) -> str:
    return re.sub('([A-Z])', lambda x: '_' + x.group(1).lower(), camel_case_str)


def main():
    _, name = sys.argv

    camel_case_name = to_camel_case(name)
    snake_case_name = to_snake_case(name)

    module_path = f'modules/{snake_case_name}'
    os.mkdir(module_path)

    with open(f'{module_path}/__init__.py', mode='w') as fp:
        fp.write(INIT_CODE_TEMPLATE % camel_case_name)

    with open(f'{module_path}/module.py', mode='w') as fp:
        fp.write(MODULE_CODE_TEMPLATE % camel_case_name)

    print(INIT_CODE_TEMPLATE % camel_case_name)
    print(MODULE_CODE_TEMPLATE % camel_case_name)


if __name__ == '__main__':
    main()
