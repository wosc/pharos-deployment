from batou.component import Component
from batou.lib.archive import Extract
from batou.lib.cmmi import Configure, Make
from batou.lib.download import Download
from batou.lib.file import Symlink
from batou_ext.apt import Package
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements


class RSSPull(Component):

    def configure(self):
        self += VirtualEnv()
        self += Requirements('rsspull.txt')
        self += Symlink(
            '/usr/local/bin/rsspull', source=self.map('bin/rsspull'))

        # TODO
        # Cronjobs
        # Add wosc to group Debian-exim


class ESniper(Component):

    version = "69675c03e17bad51c41a07e1453d897eb8c401af"  # 2.35.0
    checksum = 'sha256:79f4558b23fa43ab2314498e0abb80881cf05fca6dbead8fa054fd2fe6a9b124'

    # XXX This URL only exists after you've clicked on "download snapshot" at
    # https://sourceforge.net/p/esniper/git/ci/{version}/tree/
    url = 'https://sourceforge.net/code-snapshots/git/e/es/esniper/git.git/esniper-git-{version}.zip'

    def configure(self):
        self += Package('libssl-dev')
        self += Package('libcurl4-gnutls-dev')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        src = self._.target.replace('.zip', '')
        self += Extract(self._.target, create_target_dir=False)

        self += Patch(
            src + '/esniper.c',
            source='#define MIN_BIDTIME 5',
            target='#define MIN_BIDTIME 2')
        self += Configure(src, prefix='/usr/local')
        self += Make(src)
