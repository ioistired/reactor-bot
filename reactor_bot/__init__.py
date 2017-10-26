#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '3.1.1'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'


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

	shrug_emoji = '🦑' if april_fools() else '🤷'
	# no matter what, not knowing is always an option
	await message.add_reaction(shrug_emoji)


async def multi_poll(message):
	# the first line is the command line.
	# ignore the first line
	for line in message.content.split('\n')[1:]:
		if not line: # the line may be blank
			continue
		try:
			await message.add_reaction(get_emoji(line))
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
		return get_letter_emoji(text.upper())
	elif text in string.digits:
		return get_digit_emoji(text)
	else:
		# if not letters or digits, it's probably an emoji anyway
		return text


def get_letter_emoji(letter: str):
	if letter == 'B' and april_fools():
		return '🅱'

	start = ord('🇦')

	# position in alphabet
	letter_index = ord(letter) - ord('A')

	return chr(start + letter_index)


def get_digit_emoji(digit: str):
	return digit + '\u20E3'


def april_fools():
	today = date.today()
	return today.month == 4 and today.day == 1
