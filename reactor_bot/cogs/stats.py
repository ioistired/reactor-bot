#!/usr/bin/env python3
# encoding: utf-8

import json
import aiohttp


class StatsAPI:
	"""Various Stats APIs for bot lists
	credit to "ﾠﾠﾠﾠ#7887" on the Discord Bots List guild
	for much of this
	"""

	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession(loop=bot.loop)
		self.config_key = 'api_token'


	def __unload(self):
		self.bot.loop.create_task(self.session.close())


	async def send(self, url, headers={}, data={}):
		"""send the statistics to the API gateway."""
		async with self.session.post(
			url,
			data=data,
			headers=headers)\
		as resp:
			print('[STATS]', self.config_section, end=' ')
			if resp.status != 200:
				print('failed with status code', resp.status)
			else:
				print('response:', await resp.text())


	async def on_guild_join(self, server):
		await self.send()

	async def on_guild_remove(self, server):
		await self.send()

	async def on_ready(self):
		await self.send()


class DiscordPwStats(StatsAPI):
	config_section = 'bots.discord.pw'

	def __init__(self, *args):
		super().__init__(*args)


	async def send(self):
		await super().send(
			'https://bots.discord.pw/api/bots/{}/stats'.format(self.bot.user.id),
			data=json.dumps({'server_count': len(self.bot.guilds)}),
			headers={
				'Authorization': self.bot.config[self.config_section][self.config_key],
				'Content-Type': 'application/json'})


class DiscordBotList(StatsAPI):
	config_section = 'discordbots.org'


	def __init__(self, *args):
		super().__init__(*args)


	async def send(self):
		await super().send(
			'https://discordbots.org/api/bots/{}/stats'.format(self.bot.user.id),
			data=json.dumps({'server_count': len(self.bot.guilds)}),
			headers={
				'Authorization': self.bot.config[self.config_section][self.config_key],
				'Content-Type': 'application/json'})


class Discordlist(StatsAPI):
	config_section = 'bots.discordlist.net'


	def __init__(self, *args):
		super().__init__(*args)


	async def send(self):
		await super().send(
			'https://bots.discordlist.net/api',
			data=json.dumps({
				'token': self.bot.config[self.config_section][self.config_key],
				'server_count': len(self.bot.guilds)}),
			headers={'Content-Type': 'application/json'})


def setup(bot):
	for Cog in (DiscordPwStats, DiscordBotList, Discordlist):
		if bot.config.has_section(Cog.config_section):
			bot.add_cog(Cog(bot))
		else:
			print(
				Cog.config_section,
				"was not loaded! Please make sure it's configured properly.")
