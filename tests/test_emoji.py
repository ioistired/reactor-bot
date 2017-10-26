#!/usr/bin/env python3

from reactor_bot import emoji

from freezegun import freeze_time

class TestEmojiUtils:

	def test_extract_emoji(self):
		lines_and_emojis = {
			' M)-ystery meat': 'M',
			'🐕 dog sandwiches': '🐕',
			'3 blind mice': '3',
			'🇺🇸 flags': '🇺🇸',
			'<:python3:232720527448342530> python3!': '<:python3:232720527448342530>',
		}

		for input, output in lines_and_emojis.items():
			assert emoji.extract_emoji(input) == output


	def test_parse_emoji(self):
		io_map = {
			'<:python3:232720527448342530>': ':python3:232720527448342530',
			'a': '🇦',
			# this one's wonky--sometimes we return invalid emoji,
			# but that's ok, because Discord throws them out with an error ;)
			'123': '123⃣',
			'0': '0⃣',
			'6': '6⃣',
			'asdfghjkl;': 'asdfghjkl;',
		}

		for input, output in io_map.items():
			assert emoji.parse_emoji(input) == output


	def test_get_letter_emoji(self):
		io_map = {
			'A': '🇦',
			'B': '🇧',
			'C': '🇨',
			'D': '🇩',
			'E': '🇪',
			'F': '🇫',
			'G': '🇬',
			'H': '🇭',
			'I': '🇮',
			'J': '🇯',
			'K': '🇰',
			'L': '🇱',
			'M': '🇲',
			'N': '🇳',
			'O': '🇴',
			'P': '🇵',
			'Q': '🇶',
			'R': '🇷',
			'S': '🇸',
			'T': '🇹',
			'U': '🇺',
			'V': '🇻',
			'W': '🇼',
			'X': '🇽',
			'Y': '🇾',
			'Z': '🇿'
		}

		# one of these tests will fail on april fools
		# (hint: it's "B")
		# unless we force the date to not be april fools
		with freeze_time("2018-01-01"):
			for input, output in io_map.items():
				assert emoji.get_letter_emoji(input) == output

		with freeze_time("2018-04-01"):
			assert emoji.get_letter_emoji('B') == '🅱'

	def test_get_digit_emoji(self):
		io_map = {
			'0': '0⃣',
			'1': '1⃣',
			'2': '2⃣',
			'3': '3⃣',
			'4': '4⃣',
			'5': '5⃣',
			'6': '6⃣',
			'7': '7⃣',
			'8': '8⃣',
			'9': '9⃣',
		}

		for input, output in io_map.items():
			assert emoji.get_digit_emoji(input) == output


	def test_get_shrug_emoji(self):
		with freeze_time("2017-10-31"):
			assert emoji.get_shrug_emoji() == '🤷'
		with freeze_time("2018-04-01"):
			assert emoji.get_shrug_emoji() == '🦑'

	def test_april_fools(self):
		with freeze_time("2017-10-31"):
			assert not emoji._april_fools()
		with freeze_time("2018-04-01"):
			assert emoji._april_fools()
