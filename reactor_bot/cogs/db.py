#!/usr/bin/env python3.6
# encoding: utf-8

import logging

from aiocache import cached
import aiofiles
import asyncpg
import discord
from discord.ext import commands


logger = logging.getLogger('cogs.db')


class Database:
	def __init__(self, bot):
		self.bot = bot
		self._init_task = self.bot.loop.create_task(self._init())

	def __unload(self):
		self._init_task.cancel()

		try:
			self.pool.close()
		except AttributeError:
			pass

	async def _init(self):
		credentials = self.bot.config['database']
		# god bless kwargs
		self.pool = await asyncpg.create_pool(**credentials)

		async with aiofiles.open('data/schema.sql') as f:
			schema = await f.read()
		await self.pool.execute(schema)

		logger.info('Database connection initialized successfully')

	async def set_prefixless_channel(self, channel: int):
		statement = """
			INSERT INTO prefixless_channels
			VALUES ($1)
			ON CONFLICT DO NOTHING;"""
		await self.pool.execute(statement, channel)

	async def unset_prefixless_channel(self, channel: int):
		await self.pool.execute('DELETE FROM prefixless_channels WHERE channel = $1', channel)

	# caching this function should prevent asyncpg "operation already in progress" errors
	@cached(ttl=20, serializer=None)
	async def is_prefixless_channel(self, channel: int):
		result = await self.pool.fetchval('SELECT 1 FROM prefixless_channels WHERE channel = $1', channel)
		return bool(result)

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def prefixless(self, context, channel: discord.TextChannel, prefixless: bool):
		"""Sets a channel up to be "prefix-less".

		All messages sent in that channel will be treated as a poll.
		You must have the "Manage Roles" permission to use this command.
		"""

		func = self.set_prefixless_channel if prefixless else self.unset_prefixless_channel
		await func(channel.id)
		await context.send(
			'\N{white heavy check mark} Done. '
			'Note that it may take up to twenty seconds for your changes to take effect.')


def setup(bot):
	bot.add_cog(Database(bot))
