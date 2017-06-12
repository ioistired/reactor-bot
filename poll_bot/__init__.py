#!/usr/bin/env python3
# encoding: utf-8

"""poll_bot - A simple reaction-based Discord poll bot"""

__version__ = '0.1.0'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'
__all__ = []


import discord
from discord.ext import commands

import string
import re


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
	if len('\n'.split(message.contents)) > 1:
		multi_poll(message)
	else:
		for reaction in ('👍', '👎', '🤷'):
			await bot.add_reaction(message, reaction)


def multi_poll(message):
	# match numbers or letters with parens after
	# e.g.
	# 34)
	# 42)
	# Q)
	numbers_pattern = re.compile(r'^(\d+(?=\)))', re.IGNORECASE, re.MULTILINE)
	
	for match in re.finditer(numbers_pattern, message.contents):
		try:
			bot.add_reaction(message, get_emoji(match.group(0))
		except ValueError:
			pass


def get_emoji(text):
	if len(text) == 1:
		if text in string.ascii_letters:
			return get_regional_indicator_emoji(text.lower())
		elif text in string.digits:
			return get_digit_emoji(text)
	else:
		raise ValueError('Symbol emoji invalid or not implemented')


def get_regional_indicator_emoji(letter):
	start = ord('🇦')
	# position in alphabet
	letter_index = ord(letter) - ord('a')
	
	return chr(start + letter_index)
