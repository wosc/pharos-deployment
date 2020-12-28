from batou import UpdateNeeded
from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.supervisor import PHP
from batou_ext.user import User


class Wallabag(Component):

    version = '2.4.0'
    url = (
        'https://github.com/wallabag/wallabag/releases/download/{version}'
        '/wallabag-{version}.tar.gz')
    checksum = 'sha256:11caf6e87661215f8bb898fc61c149d8fd14de3f19928d50be53208cd5516d87'

    packages = [
        'php7.4-bcmath',
        'php7.4-curl',
        'php7.4-gd',
        'php7.4-mbstring',
        'php7.4-mysql',
        'php7.4-tidy',
        'php7.4-xml',
    ]

    db_password = None
    ui_password = None
    csrf_secret = None

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += ServiceDatabase('wallabag', password=self.db_password)
        self += Schema()
        self += AdminUser(password=self.ui_password)

        self += User('wallabag')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/wallabag', strip=1,
            owner='wallabag', group='wallabag')

        self += Patch(
            '/srv/wallabag/app/config/routing.yml',
            file='backup-api.patch', target='backup')

        self += File(
            '/srv/wallabag/app/config/parameters.yml',
            owner='wallabag', group='wallabag', mode=0o640)

        self += PHP('wallabag', user='wallabag', environ='SYMFONY_ENV=prod')

        self += File('/srv/wallabag/nginx.conf', is_template=False)
        self += VHost(self._)


class Schema(Component):

    def verify(self):
        out, _ = self.cmd('echo "show tables" | mysql -uroot wallabag')
        if not out.strip():
            raise UpdateNeeded()

    def update(self):
        with self.chdir('/srv/wallabag'):
            self.cmd(
                'sudo -u wallabag php bin/console --env=prod '
                'wallabag:install --no-interaction')


class AdminUser(Component):

    username = 'root'
    password = None

    def verify(self):
        out, _ = self.cmd(
            'echo "select username from wallabag_user" | '
            'mysql -uroot wallabag')
        if self.username not in out:
            raise UpdateNeeded()

    def update(self):
        with self.chdir('/srv/wallabag'):
            self.cmd(
                'sudo -u wallabag php bin/console --env=prod '
                'fos:user:change-password wallabag %s' % self.password)
        self.cmd(
            "echo 'update wallabag_user set username=\"{user}\", "
            "username_canonical=\"{user}\"' | mysql -uroot wallabag".format(
                user=self.username))
