from batou.component import Component, Attribute
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.file import Delete
from batou_ext.patch import Patch

from batou_ext.cron import CronTab
from batou_ext.nginx import Nginx
from batou_ext.supervisor import Supervisor


class BasePackages(Component):

    packages = Attribute('literal', """[
        'build-essential',
        'emacs-nox',
        'dnsutils',
        'git',
        'htop',
        'httpie',
        'jq',
        'mc',
        'mosh',
        'rsync',
        'screen',
        'unzip',
        'zip',
    ]""")

    def configure(self):
        for name in self.packages:
            self += Package(name)

        # Allow accessing (mostly python) software installed by batou
        self += File('/root', ensure='directory', mode=0o755)


class CronAPT(Component):

    def configure(self):
        Delete('/etc/apt/apt.conf.d/20auto-upgrades')
        self += Package('cron-apt')
        self += File(
            '/etc/cron-apt/config', source='cron-apt.conf', is_template=False)


class MySQL(Component):

    def configure(self):
        self += Package('mysql-server-5.7')
        self += Package('mysql-client-5.7')

        for name in ['backup', 'restore']:
            self += File('/usr/local/bin/mysql-%s' % name,
                         is_template=False, mode=0o755)
        self += Symlink('/etc/cron.daily/mysql-backup',
                        source='/usr/local/bin/mysql-backup')


class PHP(Component):

    def configure(self):
        self += Package('php7.2')
        self += Package('php7.2-cgi')
        # Send php errors to nginx log.
        self += Patch(
            '/etc/php/7.2/cgi/php.ini',
            source=';error_log = php_errors.log',
            target='error_log = /dev/stderr')
