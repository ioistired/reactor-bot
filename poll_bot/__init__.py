#!/usr/bin/env python3
# encoding: utf-8

"""poll_bot - A simple reaction-based Discord poll bot"""

__version__ = '0.3.0.1'
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
	if len(message.content.split('\n')) > 1:
		await multi_poll(message)
	else:
		for reaction in ('👍', '👎', '🤷'):
			await bot.add_reaction(message, reaction)


async def multi_poll(message):
	# match numbers or letters with parens after
	# e.g.
	# 1)
	# 34)
	# 42)
	# Q)
	numbers_pattern = re.compile(r'^([\d|A-Za-z]+(?=\)))', re.IGNORECASE|re.MULTILINE)
	
	for match in re.finditer(numbers_pattern, message.content):
		option = match.group(0)
		try:
			await bot.add_reaction(message, get_emoji(option))
		except ValueError as ex:
			print(ex)


def get_emoji(text):
	if len(text) > 1:
		raise ValueError('Symbol emoji "{}" invalid or not implemented'.format(text))	

	if text in string.ascii_letters:
		return get_regional_indicator_emoji(text.lower())
	elif text in string.digits:
		return get_digit_emoji(text)


def get_regional_indicator_emoji(letter):
	start = ord('🇦')
	# position in alphabet
	letter_index = ord(letter) - ord('a')
	
	return chr(start + letter_index)


def get_digit_emoji(digit):
	return digit + '\u20E3'
