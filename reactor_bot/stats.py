#!/usr/bin/env python3
# encoding: utf-8

import json
import aiohttp


class StatsAPI:
	# credit to "ﾠﾠﾠﾠ#7887" on the Discord Bots List guild
	# for much of this
	def __init__(self, bot):
		self.bot = bot
		self.session = aiohttp.ClientSession()
	
	
	def __unload(self):
		self.bot.loop.create_task(self.session.close())
	
	
	async def send(self, url, headers={}, data={}):
		"""send the statistics to the API gateway."""
		async with self.session.post(
			url,
			data=data,
			headers=headers
		) as resp:
			print('[STATS]', self.__class__.__name__, end='')
			if resp.status != 200:
				print('failed with status code', await resp.status)
			else:
				print('response:', await resp.text())

	
	async def on_server_join(self, server):
		await self.send()
	
	async def on_server_remove(self, server):
		await self.send()
	
	async def on_ready(self):
		await self.send()


class DiscordPwStats(StatsAPI):
	def __init__(self, *args):
		super().__init__(*args)


	async def send(self):
		await super().send(
			'https://bots.discord.pw/api/bots/{}/stats'.format(self.bot.user.id),
			data=json.dumps({'server_count': len(self.bot.servers)}),
			headers={
				'Authorization': self.bot.config['bots.discord.pw']['api_token'],
				'Content-Type': 'application/json',
			},
		)


class DiscordBotList(StatsAPI):
	def __init__(self, *args):
		super().__init__(*args)


	async def send(self):
		await super().send(
			'https://discordbots.org/api/bots/{}/stats'.format(self.bot.user.id),
			data=json.dumps({'server_count': len(self.bot.servers)}),
			headers={
				'Authorization': self.bot.config['discordbots.org']['api_token'],
				'Content-Type': 'application/json',
			},
		)


class Discordlist(StatsAPI):
	async def __init__(self, *args):
		super().__init__(*args)

	async def send(self):
		await super().send(
			'https://bots.discordlist.net/api',
			data=json.dumps({
				'token': self.bot.config['bots.discordlist.net']['api_token'],
				'server_count': len(self.bot.servers),
			}),
			headers={'Content-Type': 'application/json'},
		)


def setup(bot):
	for Cog in (DiscordPwStats,):
		bot.add_cog(Cog(bot))
