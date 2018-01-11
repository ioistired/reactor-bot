#!/usr/bin/env python3
# encoding: utf-8

import re
import string
from datetime import date
import random

# signifies the end of the poll emoji and start of shrug/easter eggs
# I could use None here but I wanted a descriptive name
END_OF_POLL_EMOJI = object()

def get_poll_emoji(message, shrug=True):
	"""generate the proper emoji to react to any poll message"""
	# first line is poll title / command line (ignored)
	# only get the first 19 lines, otherwise there'd be no room for 🤷
	# but if the user doesn't want shrug, get the first 20
	message = message.split('\n')[1:21 - shrug] # tbh this is a hack
	if len(message) > 0:
		for line in message:
			if line:
				yield parse_starting_emoji(line)
	else:
		yield from ('👍', '👎')

	# this is so that the receiver knows to stop
	# if no poll emoji were encountered
	yield END_OF_POLL_EMOJI

	if shrug:
		yield '🤷'

	# TODO there's no way to disable this.
	# Evaluate whether that's a good thing.
	easter_egg_emoji = get_easter_egg_emoji()
	if easter_egg_emoji is not None:
		yield easter_egg_emoji


def parse_starting_emoji(line):
	"""find text/emoji at the beginning of a line
	and convert it to proper emoji"""
	return parse_emoji(extract_emoji(line))


def extract_emoji(line):
	"""extract *unparsed* emoji from the beginning of a line
	the emoji may be separated by either ')' or whitespace"""
	return line.split(')')[0].split()[0].strip()


def parse_emoji(text):
	"""convert text to a corresponding similar emoji
	text should be a single character, unless it's a server custom emoji
	or a flag emoji

	parse_emoji is undefined if text does not meet these conditions
	"""

	# match server emoji
	custom_emoji_match = re.search(r'^<(a?:[\w_]*:\d*)>', text)

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


def get_letter_emoji(letter):
	if letter == 'B' and _date() == (4, 1):
		return '🅱'

	start = ord('🇦')

	# position in alphabet
	letter_index = ord(letter) - ord('A')

	return chr(start + letter_index)


def get_digit_emoji(digit: str):
	return digit + '\N{combining enclosing keycap}'


def get_easter_egg_emoji():
	shrug_emoji = {
		(4, 1): ('🦑', '\N{octopus}'),
		(5, 9): (':fsociety:376935242029727745',),
		(10, 31): ('\N{jack-o-lantern}', '\N{ghost}'),
	}

	shrug_emoji = shrug_emoji.get(_date())

	if shrug_emoji is not None:
		# random.choice(a) s.t. len(a) == 1 is always a[0]
		# so if there's more than one shrug emoji, pick one
		# else, use the only one available
		return random.choice(shrug_emoji)

def _date():
	today = date.today()
	return today.month, today.day
