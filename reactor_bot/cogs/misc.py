#!/usr/bin/env python3
# encoding: utf-8

from discord.ext.commands import command

class Misc:
	"""Miscellaneous commands that don't belong in any other category"""

	def __init__(self, bot):
		self.bot = bot

	@command()
	async def ping(self, context):
		"""Shows the bots latency to Discord's servers"""
		pong = '🏓 Pong! '
		start = time.time()
		message = await context.send(pong)
		rtt = (time.time() - start) * 1000
		# 10 µs is plenty precise
		await message.edit(content=pong + '│{:.2f}ms'.format(rtt))


def setup(bot):
	bot.add_cog(Misc(bot))
