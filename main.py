import sys

import toml

import modules
from lib.apache_log_analyzer import ApacheLogAnalyzer


DEFAUT_LOG_FORMAT = \
    '%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"'
# DEFAUT_LOG_FORMAT = ''


def main():
    try:
        with open('./config.toml') as fp:
            config = toml.load(fp)
    except Exception:
        print('Error: Load config failed')
        sys.exit(1)

    analyzer_config = {
        'target_files': config.get('target_files', []),
        'log_format': config.get('log_format', DEFAUT_LOG_FORMAT),
    }

    if 'range' in config:
        analyzer_config['range_min'] = config['range'].get('min', '')
        analyzer_config['range_max'] = config['range'].get('max', '')

    analyzer = ApacheLogAnalyzer(**analyzer_config)
    try:
        for module in config['modules']:
            module_class = getattr(modules, module)
            analyzer.add_module(module_class)
    except:
        print('Error: Load modules failed')
        sys.exit(1)

    results = analyzer.process()
    for result in results:
        print(result)
        print('\n' + '=' * 100 + '\n')


if __name__ == '__main__':
    main()
