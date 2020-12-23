from batou.component import Component, Attribute
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.file import Delete

from batou_ext.cron import CronTab
from batou_ext.nginx import Nginx
from batou_ext.supervisor import Supervisor


class BasePackages(Component):

    packages = Attribute('literal', """[
        'build-essential',
        'emacs-nox',
        'dnsutils',
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
