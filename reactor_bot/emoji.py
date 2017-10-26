#!/usr/bin/env python3
# encoding: utf-8

import re
import string
from datetime import date


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


def get_letter_emoji(letter: str):
	if letter == 'B' and _april_fools():
		return '🅱'

	start = ord('🇦')

	# position in alphabet
	letter_index = ord(letter) - ord('A')

	return chr(start + letter_index)


def get_digit_emoji(digit: str):
	return digit + '\u20E3'


def get_shrug_emoji():
	if _april_fools():
		return '🦑'
	else:
		return '🤷'


def _april_fools():
	today = date.today()
	return today.month == 4 and today.day == 1