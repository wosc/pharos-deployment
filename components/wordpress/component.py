from batou import UpdateNeeded
from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.cron import CronJob
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.supervisor import PHP
from batou_ext.user import User
import os
import requests


class Wordpress(Component):

    version = '5.6'
    url = 'https://wordpress.org/wordpress-{version}.tar.gz'
    checksum = 'sha256:47f466f375557bd4e3e1fff69b1ccbe29053423736b1af8f3dbf9d38c4c5fcd3'

    db_password = None
    ui_password = None

    auth_key = None
    secure_auth_key = None
    logged_in_key = None
    nonce_key = None
    auth_salt = None
    secure_auth_salt = None
    logged_in_salt = None
    nonce_salt = None

    def configure(self):
        self += Package('php8.3-mysql')

        self += User('grshop')
        self += ServiceDatabase('grshop', password=self.db_password)

        self += File('/srv/grshop/tmp', ensure='directory',
                     owner='grshop', group='grshop')

        # self += Download(
        #     self.url.format(version=self.version), checksum=self.checksum)
        # self += Extract(
        #     self._.target, target='/srv/grshop/lib', strip=1,
        #     owner='grshop', group='grshop')

        self += File(
            '/srv/grshop/lib/wp-config.php',
            owner='grshop', group='grshop', mode=0o640)

        self += File(
            '/srv/grshop/lib/wp-content/plugins'
            '/wc-free-checkout-fields/wc-free-checkout-fields.php',
            leading=True, owner='grshop', group='grshop', is_template=False)

        self += PHP(
            'grshop',
            params={
                'upload_max_filesize': '200M', 'post_max_size': '200M',
                'memory_limit': '64M', 'upload_tmp_dir': '/srv/grshop/tmp',
                'open_basedir': '/srv/grshop/lib', 'allow_url_fopen': 'Off'},
            user='grshop')

        self += File(
            '/srv/grshop/nginx.conf',
            source='nginx.conf', is_template=False)
        self += VHost(self._)

        self += AdminUser(password=self.ui_password)

        self += File('/srv/grshop/wp-cron.sh', mode=0o755,
                     owner='grshop', group='grshop')
        self += CronJob(
            '/srv/grshop/wp-cron.sh',
            user='grshop',
            timing='* * * * *',
            logger='grshop')


class AdminUser(Component):

    username = 'wosc'
    email = 'gregor@grmusik.de'
    password = None

    def verify(self):
        out, _ = self.cmd(
            'echo "select user_login from wp_users" | '
            'mysql -uroot grshop')
        if self.username not in out:
            raise UpdateNeeded()

    def update(self):
        # See <https://peteris.rocks/blog
        #   /unattended-installation-of-wordpress-on-ubuntu-server/>
        requests.post(
            'https://localhost/shop/wp-admin/install.php?step=2',
            headers={'Host': 'grmusik.de'},
            data={
                'weblog_title': 'GRShop',
                'admin_email': self.email,
                'user_name': self.username,
                'admin_password': self.password,
                'admin_password2': self.password,
                'pw_weak': '1',
            }, verify=False)


class WordpressCLI(Component):

    version = '2.7.1'
    url = 'https://github.com/wp-cli/wp-cli/releases/download/v{version}/wp-cli-{version}.phar'
    checksum = 'sha256:bbf096bccc6b1f3f1437e75e3254f0dcda879e924bbea403dff3cfb251d4e468'

    def configure(self):
        self += Download(
            self.url.format(version=self.version), checksum=self.checksum,
            target='/usr/local/bin/wp')
        self.download = self._

    def verify(self):
        self.download.assert_no_changes()

    def update(self):
        os.chmod(self.download.target, 0o755)
