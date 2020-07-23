import os
import sys
import logging

LOGLEVEL = os.getenv('LOGLEVEL', 'INFO')

numeric_level = getattr(logging, LOGLEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % LOGLEVEL)

_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(_formatter)

_consolelog = logging.getLogger('supportBot')
_consolelog.setLevel(numeric_level)
_consolelog.addHandler(stdout_handler)

_symlog = logging.getLogger('supportBot.symphony')

def LogConsoleInfo(message):
    _consolelog.info(message)


def LogConsoleError(message):
    _consolelog.error(message)


def LogSymphonyInfo(message):
    _symlog.info(message)


def LogSymphonyError(message):
    _symlog.error(message)


def LogSystemInfo(message):
    _consolelog.info(message)


def LogSystemWarn(message):
    _consolelog.warning(message)


def LogSystemError(message):
    _consolelog.error(message)