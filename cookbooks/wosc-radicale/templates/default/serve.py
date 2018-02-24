# Taken from https://github.com/Kozea/Radicale/blob/master/radicale.wsgi
import os
import radicale
import radicale.config
import radicale.log
import waitress


config_paths = []
if os.environ.get("RADICALE_CONFIG"):
    config_paths.append(os.environ["RADICALE_CONFIG"])
config = radicale.config.load(config_paths, ignore_missing_paths=False)
filename = os.path.expanduser(config.get("logging", "config"))
debug = config.getboolean("logging", "debug")
logger = radicale.log.start("radicale", filename, debug)
wsgi = radicale.Application(config, logger)
waitress.serve(
    wsgi, threads=4,
    unix_socket='/srv/radicale/http.sock', unix_socket_perms='660')
