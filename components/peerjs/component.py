from batou.component import Component
from batou.lib.download import Download
from batou.lib.file import File
from batou_ext.archive import Extract
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.supervisor import PHP
from batou_ext.user import User


class PeerJS(Component):

    version = '31d7acd1bc9424fb22fd8ff6daadddeb2235f3cf'
    url = 'https://github.com/peers/peerjs-server/archive/{version}.tar.gz'
    checksum = 'sha256:1bdc5c85dfbae29098ea16d25586f2753401a132c710f4bcbce74bb4fa169367'

    def configure(self):
        self += User('peerjs')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        self += Extract(
            self._.target, target='/srv/peerjs', strip=1,
            owner='peerjs', group='peerjs')

        self += Patch(
            '/srv/peerjs/lib/server.js',
            file='ws-3.0.patch', target='wosc patched')

        self += File('/srv/peerjs/package.json', is_template=False)
        self += File('/srv/peerjs/package-lock.json', is_template=False)
        self.packages = self._

        self += File('/srv/peerjs/serve.js', is_template=False,
                     owner='peerjs', group='peerjs')
        self += PHP(
            'peerjs',
            command='node serve.js',
            user='peerjs',
            directory='/srv/peerjs',
            dependencies=[self])

        self += File('/srv/peerjs/nginx.conf', is_template=False)
        self += VHost(self._)

    def verify(self):
        self.packages.assert_no_changes()

    def update(self):
        with self.chdir('/srv/peerjs'):
            self.cmd('sudo -Hu peerjs npm install')
