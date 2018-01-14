#!/usr/bin/env python3
# encoding: utf-8

from datetime import datetime
import time

import discord
from discord.ext.commands import command


class Meta:
	"""Commands about the bot itself."""

	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command('help')

    async def help(self, ctx, *, command: str = None):
        """Shows help about a command or the bot"""
        try:
            if command is None:
                p = await HelpPaginator.from_bot(ctx)
            else:
                entity = self.bot.get_cog(command) or self.bot.get_command(command)

                if entity is None:
                    clean = command.replace('@', '@\u200b')
                    return await ctx.send(f'Command or category "{clean}" not found.')
                elif isinstance(entity, commands.Command):
                    p = await HelpPaginator.from_command(ctx, entity)
                else:
                    p = await HelpPaginator.from_cog(ctx, entity)

            await p.paginate()
        except Exception as e:
			await ctx.send(e)

	@command()
	async def invite(self, context):
		"""Sends you a link so you can add the bot to your own server.
		Thanks! 😊
		"""
		permission_names = (
			'manage_messages', # needed to remove reactions on message edit
			'send_messages', # needed for help message
			# in case the user supplies an external emoji in a poll
			'external_emojis',
			'read_messages', # needed to act on commands
			'add_reactions', # needed to add poll options
			'embed_links') # needed to send the help message
		permissions = discord.Permissions()
		permissions.update(**dict.fromkeys(permission_names, True))

		await context.send(
			'<%s>' % discord.utils.oauth_url(self.bot.client_id, perms))


def setup(bot):
	bot.add_cog(Meta(bot))
