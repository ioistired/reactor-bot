#!/usr/bin/env python3
# encoding: utf-8

import json
from pathlib import Path

from . import ReactorBot

with open(Path(__file__).parent.parent / 'data' / 'config.json') as f:
	config = json.load(f)

bot = ReactorBot(config=config)

main = bot.run
main()
