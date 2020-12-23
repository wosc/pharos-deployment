from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.apache import CGI

from batou_ext.apache import CGIServer


class DDNS(Component):

    # How to set up a Synology SRM Router to use this service as client:
    # - Enable default "admin" account and set a password
    # - Enable SSH service and allow in firewall
    # - `ssh root@THEROUTER` using the password of the default "admin" user
    # - Add this to the /etc.defaults/ddns_provider.conf file:
    # [wosc.de]
    #   modulepath=DynDNS
    #   queryurl=https://pharos.wosc.de/dns-update?hostname=__HOSTNAME__&myip=__

    username = ''
    password = ''
    hostnames = ''

    def configure(self):
        self += VirtualEnv(path='/srv/cgiserv/ddns')
        self._ += Requirements(source='ddns/requirements.txt')

        self += File(
            '/srv/cgiserv/ddns/config',
            owner='cgiserv', group='cgiserv', mode=0o640,
            source='ddns/ddns.conf')

        self += File('/srv/cgiserv/apache.d/ddns.conf',
                     source='ddns/apache.conf', is_template=False)
        self += CGI(self._)

        self += File('/srv/cgiserv/nginx.d/ddns.conf',
                     source='ddns/nginx.conf', is_template=False)
        self += VHost(self._)


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
