from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File, SyncDirectory
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

    version = '1.6.7'
    url = (
        'https://github.com/roundcube/roundcubemail/releases/download/{version}'
        '/roundcubemail-{version}-complete.tar.gz')
    checksum = 'sha256:cf52515e65b2818cb02fd7a202c766367b8c54d8b7fea27dda9c81aa7ce1d3a6'

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

        self += User('roundcube')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/roundcube', strip=1,
            owner='roundcube', group='roundcube')
        self += Delete('/srv/roundcube/installer')

        self += File(
            '/srv/roundcube/config/config.inc.php', source='config.php',
            owner='roundcube', group='roundcube', mode=0o640)

        self += Download(
            'https://github.com/marneu/login_info/archive/'
            'b4e8a299a3f10b5e81a753a84cc9fe51015b0035.zip',
            checksum='sha256:3e90853e991dfb7e8ec1814f716ebf031633859a6c522e9281a1381b310b45e6')
        self += Extract(self._.target, owner='roundcube', group='roundcube')
        # Poor man's strip for zip, idea taken from
        # <https://github.com/chef-cookbooks/ark/blob/e8c03f6/
        #   libraries/unzip_command_builder.rb#L34>
        self += SyncDirectory(
            '/srv/roundcube/plugins/login_info',
            source=self._.target + '/*', sync_opts='-a')

        self += ServiceDatabase(
            'roundcube', password=self.db_password,
            schema='/srv/roundcube/SQL/mysql.initial.sql')

        self += PHP(
            'roundcube',
            params={'upload_max_filesize': '30M', 'post_max_size': '30M'},
            user='roundcube')

        self += File(
            '/etc/nginx/sites-available/mail.wosc.de',
            source='nginx.conf', is_template=False)
        self += VHost(self._, site_enable=True)
