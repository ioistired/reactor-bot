#!/usr/bin/env python3
# encoding: utf-8

from discord.ext import commands


class Admin:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.is_owner()
	async def reload(self, context, *, cog: str):
		cog = 'reactor_bot.cogs.' + cog

		try:
			self.bot.unload_extension(cog)
			self.bot.load_extension(cog)
		except Exception as e:
			await context.send(
				'**ERROR**: {} - {}'.format(type(e).__name__, e))
		else:
			await context.send('**SUCCESS**')


def setup(bot):
	bot.add_cog(Admin(bot))
