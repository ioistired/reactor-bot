#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '3.1.1'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'


from reactor_bot import emoji

import discord
from discord.ext import commands
import aiohttp

import re
import string
from datetime import date

bot = commands.Bot(command_prefix='poll')


@bot.event
async def on_ready():
	print('----------------------')
	print('Logged in as:')
	print('Username:', bot.user.name)
	print('ID:', bot.user.id)
	print('----------------------')


@bot.command(name=':', pass_context=True)
async def reaction_poll(context):
	message = context.message

	# multiple lines
	if message.content.count('\n') > 0:
		await multi_poll(message)
	else:
		# yes, no, shrug
		# TODO make these customizable, as some people prefer
		# :squid: to :shrug:
		for reaction in ('👍', '👎'):
			await message.add_reaction(reaction)

	# no matter what, not knowing is always an option
	await message.add_reaction(emoji.get_shrug_emoji())


async def multi_poll(message):
	# the first line is the command line.
	# ignore the first line
	for line in message.content.split('\n')[1:]:
		if not line: # the line may be blank
			continue
		try:
			await message.add_reaction(emoji.parse_starting_emoji(line))
		# since we're trying to react with arbitrary emoji,
		# some of them are going to be bunk
		# but that shouldn't stop the whole poll
		except discord.errors.HTTPException:
			continue

