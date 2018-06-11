Reactor™
========

.. image:: https://discordbots.org/api/widget/status/323505480766849026.svg?noavatar=true
	:target: https://discordbots.org/bot/323505480766849026
	:alt: Discord Bots List

The best dang Discord poll bot around™

Usage
-----

::

	poll: Is F# better than Python?

*The bot will add 👍, 👎, and 🤷 (shrug) as reactions* ::

	poll: Where should we go for pizza?
	A Domino's
	B Papa John's (papa bless)
	C Giordano's

*The bot will add 🇦, 🇧, 🇨, and 🤷 as reactions*
(You can also use numbers, but not 1234 or 10 for technical reasons)

You can also use right-parens and other emoji ::

	poll: How should I punctuate whomstve?
	🤔) whomst've
	:thonking:) whom'st've
	🅱️) w'h'o'm's't've
	

*🤔, \:thonking\: (if your server has it), 🅱️, and 🤷 will be added as reactions*


Installation
------------

Run this in :code:`psql`::

	CREATE USER reactor;
	\password reactor
	CREATE SCHEMA reactor;
	GRANT ALL PRIVILEGES ON SCHEMA reactor TO reactor;
	CREATE DATABASE reactor OWNER reactor;

And then copy data/config.example.json to data/config.json and fill out the appropriate values
in the database section and all the other sections.

Now just :code:`pip install . -r requirements.txt`, preferably inside a venv.
And finally, to run the bot, you do :code:`python -m reactor_bot`.

Compatibility
-------------

Python3.6+

License
-------

MIT. See `COPYING </COPYING>`_.

Authors
-------

Reactor was written by `Benjamin Mintz <bmintz@protonmail.com>`_.
