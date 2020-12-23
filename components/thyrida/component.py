from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User


class Thyrida(Component):

    db_password = None

    def configure(self):
        self += User('thyrida')
        self += VirtualEnv(path='/srv/thyrida/deployment')
        self._ += Requirements()
        reqs = self._

        self += File(
            '/srv/thyrida/paste.ini',
            owner='thyrida', group='thyrida', mode=0o640)

        self += Program(
            'thyrida',
            command='/srv/thyrida/deployment/bin/pserve /srv/thyrida/paste.ini',
            user='thyrida',
            dependencies=[reqs, self._])

        self += File('/srv/thyrida/nginx.conf', is_template=False)
        self += VHost(self._)
