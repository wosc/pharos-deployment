from batou.component import Component
from batou_ext.apt import AptRepository, Package


class NodeJS(Component):

    version = '22'

    def configure(self):
        self += Package('apt-transport-https')
        self += AptRepository(
            'nodesource',
            url='https://deb.nodesource.com/node_%s.x' % self.version,
            distro='nodistro',
            key='https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key')
        self += Package('nodejs')
