# Taken from https://github.com/Kozea/Radicale/blob/1.1.x/radicale.wsgi
import logging
import radicale
import radicale.log
import waitress


def wsgi(environ, start_response):
    try:
        return APP(environ, start_response)
    except Exception:
        logging.error('Uncaught exception', exc_info=True)


radicale.log.start()
APP = radicale.Application()
waitress.serve(wsgi, threads=4, listen='localhost:7076')
