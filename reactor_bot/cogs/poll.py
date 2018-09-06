#!/usr/bin/env python3
# encoding: utf-8

from string import ascii_uppercase

import discord
from discord.ext import commands
import inflect

from reactor_bot import emoji_utils as emoji

class Poll:
	"""These commands are probably what you added the bot for."""

	p = inflect.engine()

	NOSHRUG_KEYWORDS = set()
	for no in ('no', '⛔', '🚫'):
		for shrug in ('shrug', '🤷'):
			NOSHRUG_KEYWORDS.add(no+shrug)
			NOSHRUG_KEYWORDS.add(no+' '+shrug)
	NOSHRUG_KEYWORDS = frozenset(NOSHRUG_KEYWORDS)

	def __init__(self, bot):
		self.bot = bot
		self.db = self.bot.get_cog('Database')

	async def on_message(self, message):
		if not self.bot.should_reply(message):
			return

		context = await self.bot.get_context(message)

		# e.g. poll: go out for lunch?
		# or poll:foo (assuming foo is not a command)
		if (
			context.prefix and not context.command
			or not context.prefix and await self.db.is_prefixless_channel(message.channel.id)
		):
			await self.reaction_poll(message)

	async def reaction_poll(self, message):
		content = message.content

		shrug = not any(keyword in content for keyword in self.NOSHRUG_KEYWORDS)
		emoji_set = await self.db.get_poll_emoji(message.channel.id)

		seen_reactions = set()
		reactions_added = False
		for reaction in emoji.get_poll_emoji(content, shrug=shrug, emoji_set=emoji_set):
			if reaction in seen_reactions:
				continue
			elif reaction is emoji.END_OF_POLL_EMOJI:
				# after END_OF_POLL_EMOJI comes the shrug and easter egg emojis,
				# which should *not* be added if the user did not provide a valid poll.
				# example of an invalid poll:
				#
				# poll: foo
				# )
				# asdf
				# 123:
				if not seen_reactions:
					return
				# don't react with emoji.END_OF_POLL_EMOJI!
				continue
			if await self.react_safe(message, reaction):
				seen_reactions.add(reaction)

	@staticmethod
	async def react_safe(message, reaction):
		try:
			await message.add_reaction(reaction)
		except discord.errors.HTTPException:
			# since we're trying to react with arbitrary emoji,
			# some of them are going to be bunk
			# but that shouldn't stop the whole poll
			return False
		else:
			return True

	async def prompt(self, context, question, check):
		await context.send(question)
		return await self.get_response(check)

	async def get_response(self, check):
		response = await self.bot.wait_for('message', check=check)
		return response.content.strip().lower()

	async def prompt_boolean(self, context, question, check):
		yesses = {
			'yes',
			'y',
			'sure',
			'ok',
			'uh-huh',
			'yep',
			'why not'
			'true',
			'\N{check mark}',
			'\N{heavy check mark}',
			'\N{white heavy check mark}',
			'\N{ballot box with check}',
			'<:check:314349398811475968>',
			'<:Yes:359195592758394881>'}
		nos = {
			'no',
			'n',
			'false',
			'nope',
			'\N{cross mark}',
			'\N{regional indicator symbol letter x}',
			'\N{heavy multiplication x}',
			'\N{ballot box with ballot}',
			'\N{no entry}',
			'\N{no entry sign}',
			'<:xmark:314349398824058880>',
			'<:No:359195592951332874>'}

		await context.send(question)

		while True:
			response = await self.get_response(check)
			if response in yesses:
				return True
			elif response in nos:
				return False

	@commands.command(name='make')
	async def interactive_poll(self, context):
		"""Lets you make a poll by answering a series of questions.
		Useful if you don't know how to use the bot yet.
		"""
		def check(m):
			return m.author == context.author and m.channel == context.channel

		async def get_message():
			return (await self.bot.wait_for('message', check=check)).content

		message = 'poll: '

		await context.send(
			'Hoi! What would you like the title to be? '
			'To leave it blank, just say "none".')

		title = await get_message()
		message += '' if title == 'none' else title
		message += ' (created by %s)' % context.author.mention

		query = (
			'Cool, so the'
			+ ("re's no title" if title == 'none' else ' title is ' + title) + '. '
			+ 'Is this a yes/no poll?')
		boolean_poll = await self.prompt_boolean(context, query, check)

		query = 'Would you like to add a shrug emoji to the poll too?'
		shrug = await self.prompt_boolean(context, query, check)

		if not shrug:
			message += ' noshrug'
			max_options = 20
		else:
			max_options = 19

		if boolean_poll:
			await self.reaction_poll(await context.send(message))
			return

		message += '\n'
		options = []
		for i in range(1, max_options+1):
			question = self.p.inflect(
				'Alright. '
				'''What's the ordinal(%d) option? To stop, say "stop".''' % i)

			next_option = await self.prompt(context, question, check)
			if next_option.lower() == 'stop':
				break
			options.append(next_option)

		await self.reaction_poll(
			await context.send(message + self.poll_options(options)))

	@staticmethod
	def poll_options(options):
		poll_options = []
		for i, option in enumerate(options):
			poll_options.append('{} {}'.format(ascii_uppercase[i], option))
		return '\n'.join(poll_options)


def setup(bot):
	bot.add_cog(Poll(bot))
