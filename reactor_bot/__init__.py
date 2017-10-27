#!/usr/bin/env python3
# encoding: utf-8

"""reactor_bot - The best dang Discord poll bot around™"""

__version__ = '3.2.1'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'


from reactor_bot import emoji

import discord
from discord.ext import commands

import sys

bot = commands.Bot(command_prefix='poll')


@bot.event
async def on_ready():
	print('----------------------')
	print('Logged in as:')
	print('Username:', bot.user.name)
	print('ID:', bot.user.id)
	print('----------------------')


@bot.command(name=':')
async def reaction_poll(context):
	message = context.message
	seen_reactions = set()
	for reaction in emoji.get_poll_emoji(message.content):
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
