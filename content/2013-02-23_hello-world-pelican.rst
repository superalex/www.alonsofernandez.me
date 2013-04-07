Mi nuevo blog funciona con pelican
##################################

:date: 2013-02-23 20:13
:tags: pelican, python, amazon, S3
:category: Development
:slug: mi-nuevo-blog-funciona-con-pelican
:author: Alejandro Alonso
:summary: Mi nuevo blog funciona con pelican

¡Hola a todos!

Hoy inauguro blog, como no soy demasiado fan de los típicos primeros posts de "HOLA MUNDO" he decidio hacer otra cosa. Lo que voy a hacer es un post autoreferente que habla de cómo está hecho este primer post.

Después de un tiempo de darle vueltas me he decidido a usar pelican (http://pelican.readthedocs.org/), un generador estático de blogs escrito en python, hay unas cuantas razones que me han llevado a usar esta aproximación y no el clásico wordpress, ahí van las principales:

 - Seguridad: a lo largo de los años he visto muchos wordpress o similares comprometidos, un sitio totalmente estático es muchísimo más seguro.
 - No necesito un wp-admin si al final soy yo el único editor. Además puedo utilizar RST como formato para editar.
 - El alojamiento se vuelve trivial, puedo utilizar prácticamente cualquier servicio y desentenderme totalmente de la escalabilidad y el mantenimiento. Un blog como este que podría estar recibiendo cientos de miles de millones de visitas en cuestión de días (sin exagerar ni un poco) no debería morir ante un pico de carga. Si lo alojo en una de mis máquinas tengo que estar pendiente, ahora puedo utilizar las "pages" de github (http://pelican.readthedocs.org/en/3.1.1/tips.html#publishing-to-github) o por ejemplo S3 de Amazon (que es lo que estoy usando ahora mismo).

Por supuesto esta aproximación tiene sus puntos flojos:

 - Los comentarios están en disqus (http://disqus.com/), no me hace mucha gracia que los comentarios de mi blog vivan fuera pero puedo vivir con ello.
 - Las búsquedas: todo es estático, no hay un motor que me permita filtrar contenidos. Tampoco me preocupa especialmente porque siempre se puede utilizar el site: de google (http://support.google.com/websearch/bin/answer.py?hl=en&answer=136861)

La configuración de pelican es trivial y hay un montón de documentación que explica de manera sencilla todas las opciones de configuración. Siguiendo las instrucciones de http://pelican.readthedocs.org/en/3.1.1/getting_started.html tienes un blog listo en cuestión de minutos. En mi caso pasé un rato probando los themes publicados en https://github.com/getpelican/pelican-themes hasta que elegí tuxlite_tbs. Toda la configuración se gestional en un fichero pelicanconf.py, os dejo el mío para que veais cómo ha quedado.

.. code:: python

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



Un artículo bastante útil sobre pelican: http://fjavieralba.com/pelican-a-static-blog-generator-for-pythonistas.html


Para sincronizar con amazon estoy usando s3cmd, cuando quiero subir los cambios ejecuto:

.. code:: python

  s3cmd sync --acl-public --delete-removed output/ s3://alonsofernandez.me

