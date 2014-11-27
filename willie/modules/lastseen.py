# coding=utf8
"""
lastseen.py - Willie Seen Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from __future__ import unicode_literals

import time
import datetime
from willie.tools import Ddict, Nick, get_timezone, format_time
from willie.module import commands, rule, priority

seen_dict = Ddict(dict)

@commands('lastseen', 'seen')
def seen(bot, trigger):
    """Scrive quando e dove l'utente è stato visto per l'ultima volta"""
    if not trigger.group(2):
        bot.say(".seen <nick> - Scrive quando <nick> è stato visto l'ultima volta")
        return
    nick = Nick(trigger.group(2).strip())
    if nick in seen_dict:
        timestamp = seen_dict[nick]['timestamp']
        channel = seen_dict[nick]['channel']
        message = seen_dict[nick]['message']

        tz = get_timezone(bot.db, bot.config, None, trigger.nick,
                          trigger.sender)
        saw = datetime.datetime.utcfromtimestamp(timestamp)
        timestamp = format_time(bot.db, bot.config, tz, trigger.nick,
                                trigger.sender, saw)

        msg = "Ho visto %s per l'ultima volta %s su %s, e ha detto %s" % (nick, timestamp, channel, message)
        bot.say(str(trigger.nick) + ': ' + msg)
    else:
        bot.say("Mi spiace, non ho visto %s in giro." % nick)


@rule('(.*)')
@priority('low')
def note(bot, trigger):
    if not trigger.is_privmsg:
        nick = Nick(trigger.nick)
        seen_dict[nick]['timestamp'] = time.time()
        seen_dict[nick]['channel'] = trigger.sender
        seen_dict[nick]['message'] = trigger