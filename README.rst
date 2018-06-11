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


If you have a certain channel for which every message should be a poll,
you can use the command: poll:prefixless. It works like this:

:code:`poll:prefixless #channel-here yes/no`

If yes (or 1 or true), every message sent in that channel will be treated as a poll.
You need the "manage roles" permission to change this setting.


Installation
------------

Requirements
^^^^^^^^^^^^

Compatibility
-------------

License
-------

MIT. See `COPYING </COPYING>`_.

Authors
-------

Reactor was written by `Benjamin Mintz <bmintz@protonmail.com>`_.
