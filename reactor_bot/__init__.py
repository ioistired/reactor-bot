#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.5.12'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

import json
import logging
import traceback

import discord
from discord.ext import commands


logging.basicConfig(level=logging.INFO)
prefixes = (capitalization + ':' for capitalization in ('Poll', 'poll', 'POLL'))
bot = commands.Bot(
	command_prefix=commands.when_mentioned_or(*prefixes),
	activity=discord.Game(name='poll:help'),
)


with open('data/config.json') as config_file:
	bot.config = json.load(config_file)
bot.dev_mode = bot.config['release'] == 'development'
del config_file


@bot.event
async def on_ready():
	message = 'Logged in as: %s' % bot.user
	separator = '━' * len(message)
	print(separator, message, separator, sep='\n')
	bot.client_id = (await bot.application_info()).id


# based on this code:
# https://github.com/Rapptz/RoboDanny/blob/ca75fae7de132e55270e53d89bc19dd2958c2ae0/bot.py#L77-L85
# received from Rapptz, used under the MIT License.
@bot.event
async def on_command_error(context, error):
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
	elif isinstance(error, commands.CommandInvokeError):
		await context.send('An internal error occured while trying to run that command.')
		logger.error('Error in command %s:', context.command.qualified_name)
		logger.error(''.join(traceback.format_tb(error.original.__traceback__)))
		# pylint: disable=logging-format-interpolation
		logger.error('{0.__class__.__name__}: {0}'.format(error.original))


def should_reply(bot, message):
	if message.author == bot.user:
		return False
	if not bot.dev_mode and message.author.bot:
		return False
	if not message.content:
		return False

	return True


@bot.event
async def on_message(message):
	if should_reply(bot, message):
		await bot.process_commands(message)
