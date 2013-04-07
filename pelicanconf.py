#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Alejandro Alonso'
SITENAME = u'Los fantásticos mundos de Superalex'
SITEURL = 'http://alejandro.alonsofernandez.me'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'es'

DATE_FORMATS = {
    'es': '%a, %d %b %Y',
}

LOCALE = (
    'es_ES.utf8',
)

# Blogroll
LINKS =  (('Kaleidos', 'http://kaleidos.net'),
          ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
)

# Social widget
SOCIAL = (('Twitter', 'http://twitter.com/_superalex_'),
          ('Git hub', 'https://github.com/superalex'),
          ('Linked In', 'http://www.linkedin.com/in/aalonsofdez/'),
          ('Facebook', 'http://www.facebook.com/alejandroalonsofernandez'),
)

DEFAULT_PAGINATION = 5
THEME = 'themes/tuxlite_tbs'
DISQUS_SITENAME = 'superalexblog'


FEED_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'

FEED_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

STATIC_PATHS = ['images']
