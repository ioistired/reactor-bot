#!/usr/bin/env python3
# encoding: utf-8

from string import ascii_uppercase

from discord.ext import commands
import inflect

from reactor_bot import emoji_utils as emoji


class Poll:
	p = inflect.engine()

	NOSHRUG_KEYWORDS = set()
	for no in ('no', '⛔', '🚫'):
		for shrug in ('shrug', '🤷'):
			NOSHRUG_KEYWORDS.add(no+shrug)
			NOSHRUG_KEYWORDS.add(no+' '+shrug)
	NOSHRUG_KEYWORDS = frozenset(NOSHRUG_KEYWORDS)

	def __init__(self, bot):
		self.bot = bot

	@classmethod
	async def reaction_poll(cls, message):
		content = message.content
		seen_reactions = set()

		shrug = not any(keyword in content for keyword in cls.NOSHRUG_KEYWORDS)

		for reaction in emoji.get_poll_emoji(content, shrug):
			if reaction not in seen_reactions:
				seen_reactions.add(reaction)
				await cls.react_safe(message, reaction)

	@staticmethod
	async def react_safe(message, reaction):
		try:
			await message.add_reaction(reaction)
		except discord.errors.HTTPException:
			# since we're trying to react with arbitrary emoji,
			# some of them are going to be bunk
			# but that shouldn't stop the whole poll
			pass

	async def prompt(self, context, question, check):
		await context.send(question)
		return (await self.bot.wait_for('message', check=check)).content.strip()

	async def prompt_boolean(self, context, question, check):
		yesses = [
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
			'<:Yes:359195592758394881>']
		nos = [
			'no',
			'n',
			'false',
			'\N{cross mark}',
			'\N{regional indicator symbol letter x}',
			'\N{heavy multiplication x}',
			'\N{ballot box with ballot}',
			'\N{no entry}',
			'\N{no entry sign}',
			'<:xmark:314349398824058880>',
			'<:No:359195592951332874>',]

		await context.send(question)

		while True:
			response = await self.bot.wait_for('message', check=check)
			response = response.content.lower().strip()
			if response in yesses:
				return True
			elif response in nos:
				return False

	@commands.command(name='make')
	async def interactive_poll(self, context):
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
			await context.send(message + await self.poll_options(options)))

	@staticmethod
	async def poll_options(options):
		poll_options = []
		for i, option in enumerate(options):
			poll_options.append('{} {}'.format(ascii_uppercase[i], option))
		return '\n'.join(poll_options)


def setup(bot):
	bot.add_cog(Poll(bot))
