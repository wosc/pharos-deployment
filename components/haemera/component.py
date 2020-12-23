from batou import UpdateNeeded
from batou.component import Component
from batou.lib.file import File
from batou_ext.cron import CronJob
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User


class Haemera(Component):

    db_password = None

    secret = None
    username = None
    password = None

    def configure(self):
        self += User('haemera')

        self += VirtualEnv(path='/srv/haemera/deployment')
        self._ += Requirements()
        req = self._

        self += File(
            '/srv/haemera/paste.ini',
            owner='haemera', group='haemera', mode=0o640)
        config = self._

        self += ServiceDatabase('haemera', password=self.db_password)
        self += Schema()

        self += Program(
            'haemera',
            command='/srv/haemera/deployment/bin/pserve /srv/haemera/paste.ini',
            user='haemera',
            dependencies=[req, config])

        self += File('/srv/haemera/nginx.conf')
        self += VHost(self._)

        self += CronJob(
            '/srv/haemera/deployment/bin/haemera-recurrences',
            args='/srv/haemera/paste.ini#haemera',
            user='haemera',
            timing='5 0 * * *')


class Schema(Component):

    def verify(self):
        out, _ = self.cmd('echo "show tables" | mysql -uroot haemera')
        if not out.strip():
            raise UpdateNeeded()

    def update(self):
        self.cmd(
            '/srv/haemera/deployment/bin/haemera-init-db '
            '/srv/haemera/paste.ini#haemera')
