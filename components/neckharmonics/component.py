from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
from batou_ext.user import User


class Neckharmonics(Component):

    def configure(self):
        self += User('neckharmonics', home='/home/neckharmonics')
        self += File('/home/neckharmonics', ensure='directory',
                     owner='neckharmonics', group='neckharmonics')

        self += File('/etc/nginx/sites-available/neckharmonics.de',
                     source='nginx.conf', is_template=False)
        self += VHost(self._, site_enable=True)
