#!/usr/bin/env python3.6
# encoding: utf-8

import logging

import aiocache
import aiofiles
import asyncpg
import discord
from discord.ext import commands


logger = logging.getLogger('cogs.db')
cached = aiocache.cached(ttl=20, serializer=None)


class Database:
	SETTINGS_UPDATED_MESSAGE = (
		'\N{white heavy check mark} Done. '
		'Note that it may take up to twenty seconds for your changes to take effect.')

	def __init__(self, bot):
		self.bot = bot
		self._init_task = self.bot.loop.create_task(self._init())

	def __unload(self):
		self._init_task.cancel()

		try:
			self.bot.loop.create_task(self.pool.close())
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

	async def set_poll_emoji(self, channel: int, yes, no, shrug):
		# mfw no INSERT OR REPLACE in postgres
		await self.pool.execute("""
			INSERT INTO poll_emoji (channel, yes, no, shrug)
			VALUES ($1, $2, $3, $4)
			ON CONFLICT (channel)
			DO UPDATE SET
				yes   = EXCLUDED.yes,
				no    = EXCLUDED.no,
				shrug = EXCLUDED.shrug
		""", channel, yes, no, shrug)

	@cached
	async def get_poll_emoji(self, channel: int):
		return tuple(await self.pool.fetchrow("""
			SELECT yes, no, shrug
			FROM poll_emoji
			WHERE channel = $1
		""", channel))

	@commands.command(name='set-emoji')
	@commands.has_permissions(manage_emojis=True)
	async def set_poll_emoji_command(self, context, channel: discord.TextChannel, yes, no, shrug):
		"""sets the poll emoji for channel to the emojis provided

		- all three arguments must be emojis. if they are not, the poll command will silently fail.
		- you must have the Manage Emojis permission to use this
		"""
		# custom emojis must be sent without surrounding < and > for reactions
		yes, no, shrug = (x.strip('<>') for x in (yes, no, shrug))
		await self.set_poll_emoji(channel.id, yes, no, shrug)
		await context.send(self.SETTINGS_UPDATED_MESSAGE)

	async def set_prefixless_channel(self, channel: int):
		statement = """
			INSERT INTO prefixless_channels
			VALUES ($1)
			ON CONFLICT DO NOTHING;"""
		await self.pool.execute(statement, channel)

	async def unset_prefixless_channel(self, channel: int):
		await self.pool.execute('DELETE FROM prefixless_channels WHERE channel = $1', channel)

	# caching this function should prevent asyncpg "operation already in progress" errors
	@cached
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
		await context.send(self.SETTINGS_UPDATED_MESSAGE)


def setup(bot):
	bot.add_cog(Database(bot))
