#!/usr/bin/env python3

from reactor_bot import emoji

from datetime import date

from freezegun import freeze_time

class TestEmojiUtils:

	@classmethod
	def setup_class(cls):
		cls.non_holiday = date(2017, 3, 27)
		cls.april_fools = date(2017, 4, 1)
		cls.five_nine = date(2017, 5, 9)
		cls.halloween = date(2017, 10, 31)

		cls.shrug_emoji = {
			cls.non_holiday: '🤷',
			cls.april_fools: '🦑',
			cls.five_nine: ':fsociety:376004430929199114',
		}


	def test_get_poll_emoji(self):
		# TODO more test cases
		messages = {
			'poll: What should we eat for lunch?\n'
			'M)-ystery meat\n'
			'🐕 dog sandwiches\n'
			'\n'
			'3 blind mice\n'
			'🇺🇸) flags\n'
			'foo\n'
			'bar': ('🇲', '🐕', '3⃣', '🇺🇸', 'foo', 'bar'),

			'poll: Haskell lang best lang?': ('👍', '👎'),
		}

		def test(shrug_emoji):
			for message, reactions in messages.items():
				assert tuple(emoji.get_poll_emoji(message)) \
					== reactions + (shrug_emoji,)

		for date, shrug_emoji in self.shrug_emoji.items():
			with freeze_time(date):
				test(shrug_emoji)


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
		# any date that isn't a holiday will do
		with freeze_time(self.non_holiday):
			for input, output in io_map.items():
				assert emoji.get_letter_emoji(input) == output

		with freeze_time(self.april_fools):
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
		for date, shrug_emoji in self.shrug_emoji.items():
			with freeze_time(date):
				assert emoji.get_shrug_emoji() == shrug_emoji

		with freeze_time(self.halloween):
			# get the shrug emoji 100 times on halloween
			responses = {emoji.get_shrug_emoji() for _ in range(100)}
			assert len(responses) == 2 # 2 unique emoji
			# the only two responses we get should be these two
			assert len({'\N{jack-o-lantern}', '\N{ghost}'} ^ responses) == 0
