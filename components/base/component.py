from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.cron import CronTab
from batou_ext.file import Delete


class BasePackages(Component):

    packages = [
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
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)


class CronAPT(Component):

    def configure(self):
        Delete('/etc/apt/apt.conf.d/20auto-upgrades')
        self += Package('cron-apt')
        self += File(
            '/etc/cron-apt/config', source='cron-apt.conf', is_template=False)
