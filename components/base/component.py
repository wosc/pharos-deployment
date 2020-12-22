from batou.component import Component
from batou_ext.apt import Package


class BasePackages(Component):

    packages = [
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
