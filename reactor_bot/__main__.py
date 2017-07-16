#!/usr/bin/env python3
# encoding: utf-8

from . import bot

from configparser import ConfigParser
from appdirs import AppDirs
import os.path

import sys


def main():
	
	dirs = AppDirs('poll-bot', 'bmintz')
	config = ConfigParser()
	config.read(os.path.join(dirs.user_config_dir, 'poll-bot.ini'))
	
	bot.discordpw_api_token = config['bots.discord.pw']['api_token']
	bot.run(config['discord']['api_token'])
	return 0


sys.exit(main())
