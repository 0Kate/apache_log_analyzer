from importlib import import_module
from pprint import pprint

import toml

import modules
from lib.apache_log_analyzer import ApacheLogAnalyzer


DEFAUT_LOG_FORMAT = '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
# DEFAUT_LOG_FORMAT = ''


def main():
    with open('./config.toml') as fp:
        config = toml.load(fp)

    analyzer_config = {
        'target_files': config.get('target_files', []),
        'log_format': config.get('log_format', DEFAUT_LOG_FORMAT),
    }

    if 'range' in config:
        analyzer_config['range_min'] = config['range'].get('min', '')
        analyzer_config['range_max'] = config['range'].get('max', '')

    analyzer = ApacheLogAnalyzer(**analyzer_config)
    for module in config['modules']:
        module_class = getattr(modules, module)
        analyzer.add_module(module_class)

    results = analyzer.process()
    for result in results:
        print(result)
        print('\n' + '=' * 100 + '\n')


if __name__ == '__main__':
    main()
