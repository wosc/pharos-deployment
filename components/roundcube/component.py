from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.file import Delete
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.supervisor import PHP
from batou_ext.systemd import Service
from batou_ext.user import User


class Roundcube(Component):

    version = '1.7.3'
    url = (
        'https://github.com/roundcube/roundcubemail/releases/download/{version}'
        '/roundcubemail-{version}-complete.tar.gz')
    checksum = 'sha256:443cde2ea03b840ce4701fe23c273f01e68702f176d282e60248236bbb5f5f85'

    db_password = None
    store_pass_key = None

    def configure(self):
        self += Package('imapproxy')
        self += Patch(
            '/etc/imapproxy.conf',
            source='#listen_address 127.0.0.1',
            target='listen_address 127.0.0.1',
            check_source_removed=True)
        self += Service('imapproxy', action='restart', deps=self._)

        self += Package('php8.3-zip')  # for zipdownload plugin
        self += User('roundcube')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/roundcube', strip=1,
            owner='roundcube', group='roundcube')
        self += Delete('/srv/roundcube/public_html/installer.php')

        self += File(
            '/srv/roundcube/config/config.inc.php', source='config.php',
            owner='roundcube', group='roundcube', mode=0o640)
        self += File('/srv/roundcube/plugins/login_info',
                     ensure='directory', owner='roundcube', group='roundcube')
        self += File(
            '/srv/roundcube/plugins/login_info/login_info.php',
            source='login_info.php', is_template=False,
            owner='roundcube', group='roundcube')

        self += ServiceDatabase(
            'roundcube', password=self.db_password,
            schema='/srv/roundcube/SQL/mysql.initial.sql')

        self += PHP(
            'roundcube',
            params={'upload_max_filesize': '30M', 'post_max_size': '30M'},
            user='roundcube')

        self += File(
            '/etc/nginx/sites-available/mail.wosc.de',
            source='nginx.conf')
        self += VHost(self._, site_enable=True)
