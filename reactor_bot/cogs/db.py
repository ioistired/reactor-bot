#!/usr/bin/env python3.6
# encoding: utf-8

import logging

import aiofiles
import asyncpg


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
		self.pool = await asyncpg.connect(**credentials)

		async with aiofiles.open('data/schema.sql') as f:
			schema = await f.read()
		await self.pool.execute(schema)

		logger.info('Database connection initialized successfully')

	async def set_prefixless_channel(self, channel: int):
		try:
			await self.pool.execute('INSERT INTO prefixless_channels VALUES ($1);', channel)
		except asyncpg.exceptions.UniqueViolationError:
			pass  # it's ok to set a channel as prefixless twice

	async def unset_prefixless_channel(self, channel: int):
		await self.pool.execute('DELETE FROM prefixless_channels WHERE channel = $1', channel)

	async def is_prefixless_channel(self, channel: int):
		# Record object is truthy
		# None is falsy
		return bool(await self.pool.fetchval('SELECT * FROM prefixless_channels WHERE channel = $1', channel))


def setup(bot):
	bot.add_cog(Database(bot))
