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


@bot.event
async def on_command_error(context, exception):
	if isinstance(exception, commands.errors.CommandNotFound):
		# prevent poll messages like "poll:foo" from logging "foo"
		# because "foo" is sensitive end user data
		return

	logging.error('Ignoring exception in command {}:'.format(context.command))
	logging.error(_format_exception(exception))

def _format_exception(exception):
	return ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))

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
