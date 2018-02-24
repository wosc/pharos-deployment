# Taken from https://github.com/Kozea/Radicale/blob/1.1.x/radicale.wsgi
import radicale
import radicale.log
import waitress


radicale.log.start()
wsgi = radicale.Application()
waitress.serve(
    wsgi, threads=4,
    unix_socket='/srv/radicale/http.sock', unix_socket_perms='660')
