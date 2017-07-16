#!/usr/bin/env python3
# encoding: utf-8

import json
import aiohttp


class StatsAPI:
	# credit to "ﾠﾠﾠﾠ#7887" on the Discord Bots List guild
	# for much of this
	def __init__(self, bot, config):
		self.bot = bot
		self.config = config
		self.session = aiohttp.ClientSession()
	
	
	def __unload(self):
		self.bot.loop.create_task(self.session.close())
	
	
	async def send(self, config_section, config_key):
		"""send the statistics to the API gateway.
		since this process varies between APIs,
		this method should only be defined in subclasses
		"""
	
		...
	
	
	async def on_server_join(self, server):
		await self.send()
	
	async def on_server_remove(self, server):
		await self.send()
	
	async def on_ready(self):
		await self.send()
