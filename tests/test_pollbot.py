#!/usr/bin/env python3

import pytest
import poll_bot

import string

class TestPollBot:

	def test_extract_emoji(self):
		lines_and_emojis = {
			' M)-ystery meat': 'M',
			'🐕 dog sandwiches': '🐕',
			'3 blind mice': '3',
			'🇺🇸 flags': '🇺🇸',
			'<:python3:232720527448342530> python3!': '<:python3:232720527448342530>',
		}
		
		for input, output in lines_and_emojis.items():
			assert poll_bot.extract_emoji(input) == output
	
	
	def test_emojify(self):
		# custom emoji extraction is the only feature unique to emojify()
		# so we'll test the other functionality in other tests
		assert poll_bot.emojify('<:python3:232720527448342530>') == ':python3:232720527448342530'
		
		assert poll_bot.emojify('asdfghjkl;') == 'asdfghjkl;'
	
	
	def test_get_regional_indicator_emoji(self):
		regional_indicator_map = {letter: chr(ord(letter) - ord('a') + ord('🇦')) for letter in string.ascii_lowercase}
		
		for input, output in regional_indicator_map.items():
			assert poll_bot.get_regional_indicator_emoji(input) == output
	
	
	def test_get_digit_emoji(self):
		io_map = {digit: digit + '\N{combining enclosing keycap}' for digit in string.digits}
		
		for input, output in io_map.items():
			assert poll_bot.get_digit_emoji(input) == output
