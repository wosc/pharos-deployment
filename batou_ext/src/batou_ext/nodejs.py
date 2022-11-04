from batou.component import Component
from batou_ext.apt import AptRepository, Package


class NodeJS(Component):

    version = '18'

    def configure(self):
        distro, _ = self.cmd('lsb_release -s -c')
        distro = distro.strip()
        self += Package('apt-transport-https')
        self += AptRepository(
            'nodesource',
            line='deb https://deb.nodesource.com/node_%s.x %s main' % (
                self.version, distro),
            key='https://deb.nodesource.com/gpgkey/nodesource.gpg.key')
        self += Package('nodejs')
