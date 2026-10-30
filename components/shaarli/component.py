from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.archive import Extract
from batou_ext.nginx import VHost
from batou_ext.supervisor import PHP
from batou_ext.user import User


class Shaarli(Component):

    version = '0.16.5'
    url = (
        'https://github.com/shaarli/Shaarli/releases/download'
        '/v{version}/shaarli-v{version}-full.zip')
    checksum = 'sha256:794e31b77cbf7795739486ce58a1ec7ed9618e7df7aab58e8f8de9db1820ec27'

    material_version = '0.16.5'
    material = (
        'https://github.com/kalvn/Shaarli-Material/releases/download'
        '/v{version}/shaarli-material.v{version}.tar.gz')
    material_checksum = 'sha256:397992ca46f6659d3f304ddc05a5a51363cf3b96eb1fee803a099e5f6cc4ec86'

    packages = [
        'php8.5-curl',
        'php8.5-mbstring',
        'php8.5-gd',
        'php8.5-xml',
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
