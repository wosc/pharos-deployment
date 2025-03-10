from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.nginx import VHost
from batou_ext.supervisor import PHP
from batou_ext.user import User


class Shaarli(Component):

    version = '0.12.1'
    url = (
        'https://github.com/shaarli/Shaarli/releases/download'
        '/v{version}/shaarli-v{version}-full.tar.gz')
    checksum = 'sha256:f614e9baddbb5ea72b2158bbfa586b5761d17918be9a97a7bd28d7255276fc0b'

    material_version = '0.12.0'
    material = (
        'https://github.com/kalvn/Shaarli-Material/releases/download'
        '/v{version}/shaarli-material.v{version}.tar.gz')
    material_checksum = 'sha256:714b332be1e0e651e91353f7ffad0e322aea00e045645b53bebbc20a0af88db4'

    packages = [
        'php8.3-curl',
        'php8.3-mbstring',
        'php8.3-gd',
        'php8.3-xml',
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
            owner='shaarli', group='shaarli')

        self += Download(
            self.material.format(version=self.material_version),
            checksum=self.material_checksum)
        self += Extract(
            self._.target, target='/srv/shaarli/public/tpl', strip=0,
            owner='shaarli', group='shaarli')

        # Shaarli has no cli installer or usable config file, so you'll be
        # prompted through the web to set a user/password. Then log in, go to
        # "Tools / Configure your shaarli" and set theme to `material`.

        self += PHP('shaarli', user='shaarli')

        self += File('/srv/shaarli/nginx.conf', is_template=False)
        self += VHost(self._)
