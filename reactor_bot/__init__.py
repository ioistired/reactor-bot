#!/usr/bin/env python3
# encoding: utf-8

"""poll_bot - A simple reaction-based Discord poll bot"""

__version__ = '2.4.1'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'
__all__ = []


import discord
from discord.ext import commands

import re
import string
import aiohttp

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
	if len(message.content.split('\n')) > 1:
		await multi_poll(message)
	else:
		# yes, no, shrug
		# TODO make these customizable, as some people prefer
		# :squid: to :shrug:
		for reaction in ('👍', '👎'):
			await bot.add_reaction(message, reaction)
	
	# no matter what, not knowing is always an option
	await bot.add_reaction(message, '🤷')


async def multi_poll(message):	
	# the first line is the command line.
	# ignore the first line
	for line in message.content.split('\n')[1:]:
		try:
			await bot.add_reaction(message, get_emoji(line))
		# since we're trying to react with arbitrary emoji,
		# some of them are going to be bunk
		# but that shouldn't stop the whole poll
		except discord.errors.HTTPException:
			continue
		


def get_emoji(line):
	return emojify(extract_emoji(line))


def extract_emoji(line):
	return line.split(')')[0].split()[0].strip()


def emojify(text):
	# match server emoji
	custom_emoji_match = re.search(r'^<(:[\w_]*:\d*)>', text)
	
	if custom_emoji_match:
		# ignore the <> on either side
		return custom_emoji_match.group(1)
	elif text in string.ascii_letters:
		return get_regional_indicator_emoji(text.lower())
	elif text in string.digits:
		return get_digit_emoji(text)
	else:
		# if not letters or digits, it's probably an emoji anyway
		return text


def get_regional_indicator_emoji(letter: str):
	start = ord('🇦')
	
	# position in alphabet
	letter_index = ord(letter) - ord('a')
	
	return chr(start + letter_index)


def get_digit_emoji(digit: str):
	return digit + '\u20E3'
