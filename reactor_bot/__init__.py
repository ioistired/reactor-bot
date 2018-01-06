#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.4.0'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

from datetime import datetime
from string import ascii_uppercase
import sys
import time

import discord
import inflect
from discord.ext import commands

from reactor_bot import emoji

p = inflect.engine()

prefixes = [capitalization + ':' for capitalization in ('Poll', 'poll', 'POLL')]
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes))

NOSHRUG_KEYWORDS = set()
for no in ('no', '⛔', '🚫'):
	for shrug in ('shrug', '🤷'):
		NOSHRUG_KEYWORDS.add(no+shrug)
		NOSHRUG_KEYWORDS.add(no+' '+shrug)
NOSHRUG_KEYWORDS = frozenset(NOSHRUG_KEYWORDS)


@bot.event
async def on_ready():
	message = 'Logged in as: %s' % bot.user
	separator = '━' * len(message)
	print(separator, message, separator, sep='\n')
	await bot.change_presence(game=discord.Game(name='poll:help'))


# since discord.py doesn't allow for commands with no name,
# (poll: foo) we have to process them manually in that case
@bot.event
async def on_message(message):
	ctx = await bot.get_context(message)

	if ctx.prefix or bot.user in message.mentions:
		if ctx.command:
			await bot.process_commands(message)
		else:
			await reaction_poll(message)


@bot.event
async def on_message_edit(before, after):
	if any(reaction.me for reaction in before.reactions):
		await before.clear_reactions()
	await on_message(after)


async def reaction_poll(message):
	content = message.content
	seen_reactions = set()

	shrug = none(keyword in content for keyword in NOSHRUG_KEYWORDS)

	for reaction in emoji.get_poll_emoji(content, shrug):
		if reaction not in seen_reactions:
			seen_reactions.add(reaction)
			await react_safe(message, reaction)


async def react_safe(message, reaction):
	try:
		await message.add_reaction(reaction)
	except discord.errors.HTTPException:
		# since we're trying to react with arbitrary emoji,
		# some of them are going to be bunk
		# but that shouldn't stop the whole poll
		pass


async def prompt(context, question, check):
	await context.send(question)
	return (await bot.wait_for('message', check=check)).content.strip()


async def prompt_boolean(context, question, check):
	yesses = [
		'yes',
		'y',
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
		response = await bot.wait_for('message', check=check)
		response = (response
			.content
			.lower()
			.strip())
		if response in yesses:
			return True
		elif response in nos:
			return False


@bot.command(name='make')
async def interactive_poll(context):
	def check(m):
		return m.author == context.author and m.channel == context.channel

	async def get_message():
		return (await bot.wait_for('message', check=check)).content

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
	boolean_poll = await prompt_boolean(context, query, check)

	query = 'Would you like to add a shrug emoji to the poll too?'
	shrug = await prompt_boolean(context, query, check)

	if not shrug:
		message += ' noshrug'
		max_options = 20
	else:
		max_options = 19

	if boolean_poll:
		await reaction_poll(await context.send(message))
		return

	message += '\n'
	options = []
	for i in range(1, max_options+1):
		question = p.inflect(
			'Alright. '
			'''What's the ordinal(%d) option? To stop, say "stop".''' % i)

		next_option = await prompt(
			context,
			question,
			check)
		if next_option.lower() == 'stop':
			break
		options.append(next_option)

	await reaction_poll(
		await context.send(message + await poll_options(options)))


async def poll_options(options):
	poll_options = []
	for i, option in enumerate(options):
		poll_options.append('{} {}'.format(ascii_uppercase[i], option))
	return '\n'.join(poll_options)


bot.remove_command('help')

@bot.command()
async def help(context):
	embed = discord.Embed(
		title='Help for Reactor',
		timestamp=datetime.utcfromtimestamp(1514622678))

	embed.add_field(
		name='ping',
		value='Usage: `poll:ping`\n'
			+ "Shows the bots latency to Discord's servers")
	embed.add_field(
		name='Poll',
		value='Usage: `poll: <your message here>`\n'
			+ '👍, 👎, and 🤷 will be added as reactions to your message, '
			+ 'unless "noshrug" is found in the message.')
	embed.add_field(
		name='Multi poll',
		value='Usage: ```poll: [poll title]\n'
			+ '<emoji> [option 1]\n'
			+ '<emoji> [option 2]\n<emoji> [option 3]...```\n'
			+ '`<emoji>` can be a custom emote, a number, or a letter.'
			+ '\nAll the emoji you specified will be added to the message,'
			+ 'as well as :shrug:. '
			+ 'However, if you add "noshrug" or "⛔shrug" or similar, '
			+ 'anywhere in the message, :shrug: will *not* be sent.')
	embed.add_field(
		name='Poll maker',
		value='Usage: `poll:make`\n'
			+ 'The bot will ask you everything it needs to know '
			+ 'about the poll, and then send it for you.\n'
			+ "Useful if you're not sure how to use the bot yet.")

	await context.send(embed=embed)


@bot.command()
async def invite(context):
	await context.send(
		'<https://discordapp.com/oauth2/authorize'
		'?client_id={}&scope=bot&permissions=273472>'.format(bot.user.id))


@bot.command()
async def ping(context):
	pong = '🏓 Pong! '
	start = time.time()
	message = await context.send(pong)
	rtt = (time.time() - start) * 1000
	# 10 µs is plenty precise
	await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


def none(iterable):
	return not any(iterable)
