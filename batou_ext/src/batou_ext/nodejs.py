from batou.component import Component
from batou_ext.apt import AptRepository, Package


class NodeJS(Component):

    version = '14'  # see https://docs.meteor.com/install.html

    def configure(self):
        distro, _ = self.cmd('lsb_release -s -c')
        distro = distro.strip()
        self += Package('apt-transport-https')
        self += AptRepository(
            'nodesource',
            url='https://deb.nodesource.com/node_%s.x' % self.version,
            distro=distro,
            key='https://deb.nodesource.com/gpgkey/nodesource.gpg.key')
        self += Package('nodejs')
