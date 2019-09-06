"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.5.15'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

from bot_bin.bot import Bot

class ReactorBot(Bot):
	def __init__(self, **kwargs):
		super().__init__(**kwargs, setup_db=True)

	startup_extensions = (
		'reactor_bot.cogs.db',
		'reactor_bot.cogs.poll',
		'reactor_bot.cogs.meta',
		'jishaku',
		'bot_bin.stats',
		'bot_bin.debug',
		'bot_bin.misc',
		'bot_bin.sql',
	)
