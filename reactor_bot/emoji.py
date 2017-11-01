#!/usr/bin/env python3
# encoding: utf-8

import re
import string
from datetime import date
import random


def get_poll_emoji(message):
	"""generate the proper emoji to react to any poll message"""
	if message.count('\n') > 0:
		# ignore the first line, which is the command line
		for line in message.split('\n')[1:]:
			if line:
				yield parse_starting_emoji(line)
	else:
		yield from ('👍', '👎')

	# no matter what, not knowing is always an option
	# TODO make this configurable anyway
	yield get_shrug_emoji()


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


def get_letter_emoji(letter):
	if letter == 'B' and _get_holiday() == 'April Fools':
		return '🅱'

	start = ord('🇦')

	# position in alphabet
	letter_index = ord(letter) - ord('A')

	return chr(start + letter_index)


def get_digit_emoji(digit: str):
	return digit + '\N{combining enclosing keycap}'


def get_shrug_emoji():
	shrug_emoji = {
		'April Fools': '🦑',
		'Halloween': '\N{jack-o-lantern}\N{ghost}',
	}

	# random.choice(a) s.t. len(a) == 1 is always a[0]
	# so if there's more than one shrug emoji, pick one
	# else, use the only one available
	return random.choice(shrug_emoji.get(_get_holiday(), '🤷'))


def _get_holiday():
	today = date.today()

	holidays = {
		(4, 1): 'April Fools',
		(10, 31): 'Halloween',
	}

	return holidays.get((today.month, today.day))
