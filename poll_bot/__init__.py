#!/usr/bin/env python3
# encoding: utf-8

"""poll_bot - A simple reaction-based Discord poll bot"""

__version__ = '0.1.0'
__author__ = 'Benjamin Mintz <bmintz@protonmail.com>'
__all__ = []


import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='')


@bot.event
async def on_ready():

		print('-------------')
		print('Logged in as:')
		print('Username:', bot.user.name)
		print('ID:', bot.user.id)
		print('-------------')


@bot.command(name='poll:', pass_context=True)
async def reaction_poll(context):

	message = context.message
	for reaction in ('👍', '👎', '🤷'):
		await bot.add_reaction(message, reaction)
