from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User


class CalibreView(Component):

    cookie_secret = None

    def configure(self):
        self += User('calibreview')

        self += VirtualEnv(path='/srv/calibreview/deployment')
        self._ += Requirements()
        req = self._

        self += File(
            '/srv/calibreview/paste.ini',
            owner='calibreview', group='calibreview', mode=0o640)
        config = self._

        self += Program(
            'calibreview',
            command='/srv/calibreview/deployment/bin/pserve /srv/calibreview/paste.ini',
            user='calibreview',
            dependencies=[req, config])

        self += File('/srv/calibreview/nginx.conf')
        self += VHost(self._)
