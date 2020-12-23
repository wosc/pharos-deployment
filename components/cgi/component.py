from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
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


class WebPasswd(Component):

    def configure(self):
        self += VirtualEnv(path='/srv/cgiserv/passwd')
        self._ += Requirements(source='passwd.txt')

        self += File(
            '/etc/sudoers.d/webpasswd',
            content='cgiserv ALL=(root) NOPASSWD: /srv/cgiserv/passwd/bin/webpasswd-change\n')

        self += File(
            '/srv/cgiserv/apache.d/passwd.conf',
            content='ScriptAlias /passwd /srv/cgiserv/passwd/bin/webpasswd-cgi\n' )
        self += CGI(self._)

        self += File(
            '/srv/cgiserv/nginx.d/passwd.conf',
            content='location /passwd { proxy_pass http://cgi; }\n')
        self += VHost(self._)
