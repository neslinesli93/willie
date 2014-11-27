# coding=utf8
"""
help.py - Willie Help Module
Copyright 2008, Sean B. Palmer, inamidst.com
Copyright © 2013, Elad Alfassa, <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

http://willie.dftba.net
"""
from __future__ import unicode_literals

from willie.module import commands, rule, example, priority
from willie.tools import iterkeys


def setup(bot=None):
    if not bot:
        return

    if (bot.config.has_option('help', 'threshold') and not
            bot.config.help.threshold.isdecimal()):  # non-negative integer
        from willie.config import ConfigurationError
        raise ConfigurationError("Attribute threshold of section [help] must be a nonnegative integer")


@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@example('.help tell')
@commands('help')
@priority('low')
def help(bot, trigger):
    """Fa vedere la documentazione di un comando, e se c'è un esempio."""
    if not trigger.group(2):
        bot.reply('Scrivi .help <comando> (ad esempio .help c) per avere info sul comando, o .commands per una lista di tutti icomandi.')
    else:
        name = trigger.group(2)
        name = name.lower()

        if bot.config.has_option('help', 'threshold'):
            threshold = int(bot.config.help.threshold)
        else:
            threshold = 3

        if name in bot.doc:
            if len(bot.doc[name][0]) + (1 if bot.doc[name][1] else 0) > threshold:
                if trigger.nick != trigger.sender:  # don't say that if asked in private
                    bot.reply('L\'help di questo comando è troppo lungo, te lo mando in query.')
                msgfun = lambda l: bot.msg(trigger.nick, l)
            else:
                msgfun = bot.reply

            for line in bot.doc[name][0]:
                msgfun(line)
            if bot.doc[name][1]:
                msgfun('e.g. ' + bot.doc[name][1])
        else:
            bot.reply("Non conosco questo comando")


@commands('commands')
@priority('low')
def commands(bot, trigger):
    """Ritorna la lista dei comandi supportati"""
    names = ', '.join(sorted(iterkeys(bot.doc)))
    if not trigger.is_privmsg:
        bot.reply("Ti sto mandando tutti i comandi in query")
    bot.msg(trigger.nick, 'Comandi: ' + names + '.', max_messages=10)
    bot.msg(trigger.nick, ("Per aiuto sui singoli comandi, fai '%s: help comando'") % bot.nick)


@rule('$nick' r'(?i)help(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
    response = (
        'Ciao, io sono un bot. Scrivimi ".commands" in query per una lista ' +
        'dei comandi supportati, o visita http://willie.dftba.net per i ' +
        'dettagli tecnici. Il mio padrone è %s.'
    ) % bot.config.owner
    bot.reply(response)
