#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.5.15'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

import contextlib
import json
import logging
import traceback

import discord
from discord.ext import commands

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('bot')

class ReactorBot(commands.Bot):
	def __init__(self):
		prefixes = (capitalization + ':' for capitalization in ('Poll', 'poll', 'POLL'))
		bot = super().__init__(
			command_prefix=commands.when_mentioned_or(*prefixes),
			activity=discord.Game(name='poll:help'),
		)

		with open('data/config.json') as config_file:
			self.config = json.load(config_file)
		self.dev_mode = self.config['release'] == 'development'

	async def on_ready(self):
		message = 'Logged in as: %s' % self.user
		separator = '━' * len(message)
		print(separator, message, separator, sep='\n')
		self.client_id = (await self.application_info()).id

	# based on this code:
	# https://github.com/Rapptz/RoboDanny/blob/ca75fae7de132e55270e53d89bc19dd2958c2ae0/bot.py#L77-L85
	# received from Rapptz, used under the MIT License.
	async def on_command_error(self, context, error):
		if isinstance(error, commands.CommandNotFound):
			# prevent poll messages like "poll:foo" from logging "foo"
			# because "foo" is sensitive end user data
			return
		if isinstance(error, commands.NoPrivateMessage):
			await context.author.send('This command cannot be used in private messages.')
		elif isinstance(error, commands.DisabledCommand):
			message = 'Sorry. This command is disabled and cannot be used.'
			try:
				await context.author.send(message)
			except discord.Forbidden:
				await context.send(message)
		elif isinstance(error, commands.UserInputError):
			await context.send(error)
		elif isinstance(error, commands.NotOwner):
			logger.error('%s tried to run %s but is not the owner', context.author, context.command.name)
			with contextlib.suppress(discord.HTTPException):
				await context.message.add_reaction(':error:487322218989092889')
		elif isinstance(error, commands.CommandInvokeError):
			await context.send('An internal error occured while trying to run that command.')
			logger.error('Error in command %s:', context.command.qualified_name)
			logger.error(''.join(traceback.format_tb(error.original.__traceback__)))
			# pylint: disable=logging-format-interpolation
			logger.error('{0.__class__.__name__}: {0}'.format(error.original))

	def should_reply(self, message):
		if message.author == self.user:
			return False
		if not self.dev_mode and message.author.bot:
			return False
		if not message.content:
			return False

		return True

	async def on_message(self, message):
		if self.should_reply(message):
			await self.process_commands(message)

	async def process_commands(self, message):
		# overridden because the default process_commands ignores bots now
		context = await self.get_context(message)
		await self.invoke(context)
