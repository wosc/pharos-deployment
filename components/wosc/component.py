from batou.component import Component
from batou.lib.file import Symlink
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
