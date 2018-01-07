#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '4.4.0'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'

from datetime import datetime
import sys
import time

import discord
import inflect
from discord.ext import commands

from reactor_bot import emoji_utils as emoji
from reactor_bot.cogs.poll import Poll

prefixes = [capitalization + ':' for capitalization in ('Poll', 'poll', 'POLL')]
bot = commands.Bot(command_prefix=commands.when_mentioned_or(*prefixes))


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
	context = await bot.get_context(message)

	if context.prefix or bot.user in message.mentions:
		if context.command:
			await bot.process_commands(message)
		else:
			await Poll.reaction_poll(message)


@bot.event
async def on_message_edit(before, after):
	if any(reaction.me for reaction in before.reactions):
		await before.clear_reactions()
	await on_message(after)


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
	permission_names = (
		'manage_messages', # needed to remove reactions on message edit
		'send_messages', # needed for help message
		# in case the user supplies an external emoji in a poll
		'external_emojis',
		'read_messages', # needed to act on commands
		'add_reactions') # needed to add poll options
	permissions = discord.Permissions()
	permissions.update(**dict.fromkeys(permission_names, True))

	await context.send(
		'<https://discordapp.com/oauth2/authorize'
		'?client_id={}&scope=bot&permissions={}>'
			.format(bot.user.id, permissions.value))


@bot.command()
async def ping(context):
	pong = '🏓 Pong! '
	start = time.time()
	message = await context.send(pong)
	rtt = (time.time() - start) * 1000
	# 10 µs is plenty precise
	await message.edit(content=pong + '│{:.2f}ms'.format(rtt))
