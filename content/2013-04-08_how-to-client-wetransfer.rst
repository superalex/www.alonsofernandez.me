Creando un cliente para wetransfer
##################################

:date: 2013-04-08 10:10
:tags: wetransfer, python, requests
:category: Development
:slug: creando-un-cliente-para-wetransfer
:author: Alejandro Alonso
:summary: Creando un cliente para we transfer

Wetransfer (https://www.wetransfer.com) es un servicio gratuito que nos permite compartir ficheros de hasta 2 gigas sin ningún tipo de registro, es bastante cómodo porque además te avisa cuando la persona con la que compartiste el archivo lo ha descargado y estos se borran automáticamente a las dos semanas (a menos que tengas una cuenta de pago). Estas características junto con una interfaz casi espartana y ultra fácil de usar lo hacen una buena opción para intercambiar archivos con clientes, de hecho fue uno de ellos el que me hizo conocer el servicio hace un tiempo.

Ahora bien, resulta que no tienen una API pública y que no hay una manera directa de poder descargar los archivos en modo linea de comandos. Para un usuario estándar que usa el navegador para descargar un fichero no es un problema pero hay situaciones en las que puede ser algo incómodo.

Veamos un ejemplo: imaginemos que Batman (sí, Batman es el nombre de mi cliente) comparte un fichero de 2 gigas conmigo, pongamos que son unos ficheros que tiene que servir su plataforma web. Esos ficheros tienen que acabar en un servidor remoto al que solamente se puede acceder en modo consola, parece que la única opción es que descargue los 2 gigas a mi máquina y desde ahí los suba al servidor, lo malo es que el ancho de banda de mi casa es bastante malo y eso dura una eternidad. Por otro lado, el ancho de banda de bajada el servidor es brutal, si pudiera descargar esos 2 gigas directamente desde wetransfer todo el proceso tardaría minutos frente a las muchas horas que llevaría la otra opción.

Con todo esto me puse a investigar a ver porqué mi navegador puede descargar ficheros y mi wget no :)

Lo primero es lo primero, cuando alguien comparte con nosotros un fichero recibimos un enlace de la forma:

.. code:: html

    https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZZ

Si visito esa url y echamos un vistazo a las peticiones que hace nuestro navegador vemos que lo primero que se hace es un GET a

.. code:: html

    https://www.wetransfer.com/api/v1/transfers/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/download?recipient_id=YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY&security_hash=ZZZZZZ&password=&ie=false

¡Vaya!, parece que al final sí que hay una API XD

La respuesta al servidor a esta llamada puede ser de dos sabores, en el primer sabor el servidor nos devuelve directamente la url de un fichero. Con esto sí que podemos hacer un wget de ese direct_link que la API nos devuelve.

.. image:: static/images/2013-04-08_how-to-client-wetransfer/we0.png
   :alt: We transfer API get


En el segundo sabor hay algo más de chicha y lo que nos interesa es el formdata de la respuesta, veamoslo en detalle:

.. image:: static/images/2013-04-08_how-to-client-wetransfer/we1.png
   :alt: We transfer API get

.. code:: json

    {"formdata":{
        "action":"https://download-dpv0zp1e09jdpwsqj0g9dwe0w.wetransfer.com/download/",
        "method":"POST",
        "enctype":"application/x-www-form-urlencoded"},
        "fields":{
            "unique":"00d8e4303847a67446a66b379fa649af20130407131900",
            "profile":"wetransfer",
            "filename":"wetransfer-test",
            "expiration":"1365344426",
            "escaped":"false",
            "signature":"90512687b064f6c31a3d88ceb4f22185733749a4d28f7f2802b9f5748a7504ef",
            "callback":"{\"formdata\":{\"action\":\"https://www.wetransfer.com/api/v1/transfers/00d8e4303847a67446a66b379fa649af20130407131900/recipients/e8f1fd990adb54e9bc50b195153c06a220130407131900\"},\"form\":{\"status\":[\"param\",\"status\"]}}"
        }
    }

¡Curioso!, parece que nos está dando información sobre a donde tendríamos que hacer un POST con una serie de parámetros...¿qué será?, ¿puede ser la url definitiva para descargar el fichero?...

Comprobemos que pasa con la última petición que la web hace para descargar el fichero:

.. image:: static/images/2013-04-08_how-to-client-wetransfer/we2.png
   :alt: We transfer API get

En este caso se está haciendo un POST a la url ACTION que nos devolvió la API pasando como parámetros todo lo que el formdata de la respuesta tenía en fields. Así que, efectivamente, la API nos devuelve la información sobre cómo pedir el fichero a descargar. Si por curiosidad hacemos varias llamadas a esta API vemos que los campos del formdata van cambiando...Tiene pinta de que por cada llamada a api/v1/transfers se generan unos valores diferentes para el formdata de manera que no podamos reusar un único enlace de descarga.

Viendo cómo funciona, nuestro programa tendría que hacer hacer una llamada a api/v1/transfers con los parámetros adecuados extraidos a partir de la url del fichero. En función de la respuesta de la API habría que hacer dos cosas:

 - Si nos devuelve un direct_link descargar directamente ese fichero
 - Si no, hacer un post al action del formdata pasando como parámetros todos los fields

Mi implementación usa python con requests, una librería muy útil para hacer peticiones web, el código está publicado en github en https://github.com/superalex/py-wetransfer y se utiliza con:

.. code:: json

    python wetransfer.py -u https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZZ

El contenido del fichero wetransfer.py debería ser el siguiente:

.. code:: python

    from urlparse import urlparse, parse_qs
    import requests, sys, json, re, getopt

    def download(file_id, recipient_id, security_hash):
        url = "https://www.wetransfer.com/api/v1/transfers/{0}/download?recipient_id={1}&security_hash={2}&password=&ie=false".format(file_id, recipient_id, security_hash)

        r = requests.get(url)
        download_data = json.loads(r.content)
        print "Downloading..."
        if download_data.has_key('direct_link'):
            content_info_string = parse_qs(urlparse(download_data['direct_link']).query)['response-content-disposition'][0]
            file_name = re.findall('filename="(.*?)"', content_info_string)[0]
            r = requests.get(download_data['direct_link'])
        else:
            file_name = download_data['fields']['filename']
            r = requests.post(download_data['formdata']['action'], data=download_data["fields"])

        output_file = open(file_name, 'w')
        output_file.write(r.content)
        output_file.close()
        print "Finished! {0}".format(file_name)

    def usage():
        print """
    You should have a we transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ

    So execute:
        python wetransfer.py -u https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZ

    And download it! :)
    """
        sys.exit()

    def main(argv):
        try:
            opts, args = getopt.getopt(argv, "u:h", ['url', 'help'])
            url = None
            for opt, arg in opts:
                if opt in ('-u', '--url'):
                    url = arg
                if opt in ('-h', '--help'):
                    usage()

            if not url:
                usage()

            [file_id, recipient_id, security_hash] = url.split('/')[-3:]
            download(file_id, recipient_id, security_hash)

        except getopt.GetoptError:
            usage()
            sys.exit(2)

    if __name__ == "__main__":
        main(sys.argv[1:])


