from batou.component import Component, Attribute, ConfigString
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.file import Delete
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.user import User, GroupMember
from batou_ext.cron import CronTab
from batou_ext.nginx import Nginx
from batou_ext.nodejs import NodeJS
from batou_ext.supervisor import Supervisor


class BasePackages(Component):

    packages = Attribute('literal', ConfigString("""[
        'build-essential',
        'emacs-nox',
        'dnsutils',
        'git',
        'htop',
        'httpie',
        'jq',
        'mc',
        'mosh',
        'python3-dev',
        'python-is-python3',
        'rsync',
        'screen',
        'unzip',
        'zip',
    ]"""))

    def configure(self):
        for name in self.packages:
            self += Package(name)

        # Allow accessing (mostly python) software installed by batou
        self += File('/root', ensure='directory', mode=0o755)

        self += User('wosc', home='/home/wosc')
        self += GroupMember('sudo', user='wosc')

        self += File('/etc/motd', is_template=False)
        self += File(
            '/etc/ssh/sshd_config.d/cyberduck.conf', source='ssh.conf',
            is_template=False)


class CronAPT(Component):

    def configure(self):
        self += Delete('/etc/apt/apt.conf.d/20auto-upgrades')
        self += Package('cron-apt')
        self += File(
            '/etc/cron-apt/config', source='cron-apt.conf', is_template=False)


class MySQL(Component):

    packages = [
        'mysql-server-8.0',
        'mysql-client-8.0',
        'libmysqlclient-dev',
        'pkg-config',  # for python package `mysqlclient`
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        for name in ['backup', 'restore']:
            self += File('/usr/local/bin/mysql-%s' % name,
                         is_template=False, mode=0o755)
        self += Symlink('/etc/cron.daily/mysql-backup',
                        source='/usr/local/bin/mysql-backup')


class PHPBase(Component):

    version = '8.3'

    def configure(self):
        self += Package('php%s' % self.version)
        self += Package('php%s-cgi' % self.version)
        # Send php errors to nginx log.
        self += Patch(
            '/etc/php/%s/cgi/php.ini' % self.version,
            source=';error_log = php_errors.log',
            target='error_log = /dev/stderr')


class Pharos(Component):

    def configure(self):
        self += File('/etc/nginx/sites-available/pharos.wosc.de',
                     source='pharos.conf', is_template=False)
        self += VHost(self._, site_enable=True)
