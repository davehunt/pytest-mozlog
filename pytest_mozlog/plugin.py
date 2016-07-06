# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import mozlog


def pytest_addoption(parser):
    group = parser.getgroup('mozlog')

    for name, (_class, _help) in mozlog.commandline.log_formatters.iteritems():
        group.addoption('--log-{0}'.format(name), action='append', help=_help)

    formatter_options = mozlog.commandline.fmt_options.iteritems()
    for name, (_class, _help, formatters, action) in formatter_options:
        for formatter in formatters:
            if formatter in mozlog.commandline.log_formatters:
                group.addoption(
                    '--log-{0}-{1}'.format(formatter, name),
                    action=action,
                    help=_help)


def pytest_configure(config):
    if not hasattr(config, 'slaveinput'):
        config.pluginmanager.register(MozLog())


class MozLog(object):

    def __init__(self):
        self.results = {}

    def pytest_configure(self, config):
        args = {}
        formatters = mozlog.commandline.log_formatters.iteritems()
        for name, (_class, _help) in formatters:
            argname = 'log_{0}'.format(name)
            if config.getoption(argname):
                args[argname] = config.getoption(argname)

        formatter_options = mozlog.commandline.fmt_options.iteritems()
        for name, (_class, _help, formatters, action) in formatter_options:
            for formatter in formatters:
                if formatter in mozlog.commandline.log_formatters:
                    argname = 'log_{0}_{1}'.format(formatter, name)
                    if config.getoption(argname):
                        args[argname] = config.getoption(argname)

        mozlog.commandline.setup_logging('pytest', args)
        self.logger = mozlog.get_default_logger(component='pytest')

    def pytest_sessionstart(self, session):
        self.logger.suite_start([])

    def pytest_sessionfinish(self, session, exitstatus):
        self.logger.suite_end()

    def pytest_runtest_logstart(self, nodeid, location):
        self.logger.test_start(nodeid)

    def pytest_runtest_logreport(self, report):
        test = report.nodeid
        status = expected = 'PASS'
        if hasattr(report, 'wasxfail'):
            expected = 'FAIL'
            if report.skipped:
                status = 'FAIL'
        elif report.failed:
            status = 'FAIL' if report.when == 'call' else 'ERROR'
        elif report.skipped:
            status = expected = 'SKIP'
        if status != expected:
            self.results[test] = (status, expected)
        if report.when == 'teardown':
            status, expected = self.results.get(test, ('PASS', 'PASS'))
            self.logger.test_end(test, status, expected)
