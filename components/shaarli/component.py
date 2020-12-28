from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.nginx import VHost
from batou_ext.supervisor import PHP
from batou_ext.user import User


class Shaarli(Component):

    version = '0.11.0'
    url = (
        'https://github.com/shaarli/Shaarli/releases/download'
        '/v{version}/shaarli-v{version}-full.tar.gz')
    checksum = 'sha256:530c26fcc7a93b72eb5a7332b3a7c6ef2deeb6dcf323b25922e7d9a720136af4'

    material = (
        'https://github.com/kalvn/Shaarli-Material/releases/download'
        '/v{version}/shaarli-material.v{version}.tar.gz')
    material_checksum = 'sha256:b0fa6116b47fb335f13e6561dbb6446d25a558256d0cd59c067d401d411a5c7a'

    packages = [
        'php7.2-curl',
        'php7.2-gd',
        'php7.2-gettext',
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += User('shaarli')

        self += File('/srv/shaarli/public', ensure='directory',
                     owner='shaarli', group='shaarli')
        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/shaarli/public', strip=1,
            owner='shaarli', group='shaarli', create_target_dir=False)

        self += Download(
            self.material.format(version=self.version),
            checksum=self.material_checksum)
        self += Extract(
            self._.target, target='/srv/shaarli/public/tpl', strip=0,
            owner='shaarli', group='shaarli', create_target_dir=False)

        # Shaarli has no cli installer or usable config file, so you'll be
        # prompted through the web to set a user/password. Then log in, go to
        # "Tools / Configure your shaarli" and set theme to `material`.

        self += PHP('shaarli', user='shaarli')

        self += File('/srv/shaarli/nginx.conf', is_template=False)
        self += VHost(self._)
