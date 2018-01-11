#!/usr/bin/env python3
# encoding: utf-8

from datetime import datetime
import time

import discord
from discord.ext.commands import command


class Misc:
	def __init__(self, bot):
		self.bot = bot
		bot.remove_command('help')

	@command()
	async def help(self, context):
		embed = discord.Embed(
			title='Help for Reactor',
			timestamp=datetime.utcfromtimestamp(1515291012))

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
		embed.add_field(
			name='invite',
			value='Usage: `poll:invite`\n'
				+ 'Sends you an invite link '
				+ 'so you can add the bot to your own server')
		embed.add_field(
			name='ping',
			value='Usage: `poll:ping`\n'
				+ "Shows the bots latency to Discord's servers")

		await context.send(embed=embed)

	@command()
	async def invite(self, context):
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
				.format(self.bot.user.id, permissions.value))

	@command()
	async def ping(self, context):
		pong = '🏓 Pong! '
		start = time.time()
		message = await context.send(pong)
		rtt = (time.time() - start) * 1000
		# 10 µs is plenty precise
		await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


def setup(bot):
	bot.add_cog(Misc(bot))
