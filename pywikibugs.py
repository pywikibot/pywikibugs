#!/usr/bin/python
# (C) Legoktm, 2013
# (C) Pywikipediabot team, 2013
# Released under the MIT License
from __future__ import unicode_literals
import re
import requests
from mtirc import bot, hooks, settings

config = dict(settings.config)
config['nick'] = 'pywikibugs'
config['debug'] = False
config['disable_on_errors'] = None
config['connections']['card.freenode.net']['channels'] = ['#mediawiki', '#pywikipediabot', '##legoktm-bots-chatter']

COLOR_RE = re.compile(r'(?:\x02|\x03(?:\d{1,2}(?:,\d{1,2})?)?)')
THINGY = re.compile('bugzilla\.wikimedia\.org/(\d*?) ')


def on_msg(**kw):
    if kw['sender'].nick.startswith('wikibugs'):
        if 'Pywikibot' in kw['text']:
            kw['bot'].queue_msg('#pywikipediabot', kw['text'])
        else:
            de_colored = COLOR_RE.sub('', kw['text'])
            match = THINGY.search(de_colored)
            if match:
                bug_id = match.group(1)
                url = 'http://bugzilla.wikimedia.org/show_bug.cgi?id=' + bug_id.strip()
                r = requests.get(url)
                if 'describecomponents.cgi?product=Pywikibot' in r.text:
                    kw['bot'].queue_msg('#pywikipediabot', kw['text'])


hooks.add_hook('on_msg', 'pywikibugs', on_msg)
if __name__ == '__main__':
    b = bot.Bot(config)
    b.run()
