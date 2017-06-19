#!/usr/bin/env python3
# encoding: utf-8

"""poll_bot - A simple reaction-based Discord poll bot"""

__version__ = '0.4.0'
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
		# yes, no, shrug
		# TODO make these customizable, as some people prefer
		# :squid: to :shrug:
		for reaction in ('👍', '👎', '🤷'):
			await bot.add_reaction(message, reaction)


async def multi_poll(message):
	numbers_pattern = re.compile(
		r'''
		
		^(\d+ # match 1 or more digits (for the 1234 emoji)...
		|. # or one of any other character
		(?=\)) # but only if there's a literal ")" afterwards
		)
		''',
		
		re.IGNORECASE|re.MULTILINE|re.VERBOSE)
	
	for match in re.finditer(numbers_pattern, message.content):
		option = match.group(0)
		print(option)
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
	else:
		# if not letters or digits, it's probably an emoji anyway
		return text


def get_regional_indicator_emoji(letter):
	start = ord('🇦')
	# position in alphabet
	letter_index = ord(letter) - ord('a')
	
	return chr(start + letter_index)


def get_digit_emoji(digit):
	return digit + '\u20E3'
