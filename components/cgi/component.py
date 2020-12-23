from batou.component import Component
from batou.lib.file import File
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.apache import CGI

from batou_ext.apache import CGIServer


class UptimeRobot(Component):

    api_key = ''

    def configure(self):
        self += VirtualEnv(path='/srv/cgiserv/uptimerobot')
        self._ += Requirements(source='uptimerobot/requirements.txt')

        self += File(
            '/srv/cgiserv/uptimerobot/config',
            owner='cgiserv', group='cgiserv', mode=0o640,
            source='uptimerobot/uptimerobot.conf')

        self += File('/srv/cgiserv/apache.d/uptimerobot.conf',
                     source='uptimerobot/apache.conf', is_template=False)
        self += CGI(self._)
