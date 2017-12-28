#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.2.1'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

from datetime import datetime
import sys
import time

import discord
from discord.ext import commands

from reactor_bot import emoji


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


async def reaction_poll(message):
	content = message.content
	seen_reactions = set()

	shrug = none(keyword in content for keyword in NOSHRUG_KEYWORDS)

	for reaction in emoji.get_poll_emoji(content, shrug):
		if reaction not in seen_reactions:
			seen_reactions.add(reaction)
			await react_safe(message, reaction)


@bot.command()
async def ping(context):
	pong = '🏓 Pong! '
	start = time.time()
	message = await context.send(pong)
	rtt = (time.time() - start) * 1000
	# 10 µs is plenty precise
	await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


async def react_safe(message, reaction):
	try:
		await message.add_reaction(reaction)
	except discord.errors.HTTPException:
		# since we're trying to react with arbitrary emoji,
		# some of them are going to be bunk
		# but that shouldn't stop the whole poll
		pass


bot.remove_command('help')

@bot.command()
async def help(context):
	embed = discord.Embed(
		title='Help for Reactor',
		timestamp=datetime.utcfromtimestamp(1514021784))

	embed.add_field(
		name='ping',
		value='Usage: `poll:ping`\n'
			+ "Shows the bots latency to Discord's servers")
	embed.add_field(
		name='Poll',
		value='Usage: `poll: <your message here>`\n'
			+ '👍, 👎, and 🤷 will be added as reactions to your message.')
	embed.add_field(
		name='Multi poll',
		value='Usage: ```poll: [poll title]\n'
			+ '<emoji> [option 1]\n'
			+ '<emoji> [option 2]\n<emoji> [option 3]...```\n'
			+ '`<emoji>` Can be a custom emote, a number, or a letter.'
			+ '\nAll the emoji you specified will be added to the message,'
			+ 'as well as :shrug:')

	await context.send(embed=embed)


def none(iterable):
	return not any(iterable)
