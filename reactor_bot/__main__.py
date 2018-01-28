#!/usr/bin/env python3
# encoding: utf-8

from . import bot

from configparser import ConfigParser
from appdirs import AppDirs
import os.path

import sys


def main():

    dirs = AppDirs('reactor-bot', 'bmintz')
    config = ConfigParser()
    config.read(os.path.join(dirs.user_config_dir, 'reactor-bot.ini'))

    bot.config = config

    # place the extensions in order of priority
    for extension in ('poll', 'misc', 'admin', 'stats'):
        print('Loading extension', extension)
        try:
            bot.load_extension('reactor_bot.cogs.' + extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(config['discord']['api_token'])
    return 0


sys.exit(main())
