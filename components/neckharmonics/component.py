from batou import UpdateNeeded
from batou.component import Component
from batou.lib.file import File, Presence, Owner, Group, Mode
from batou_ext.apache import CGI
from batou_ext.cron import CronJob
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.user import User, GroupMember
import batou.lib.git
import os.path


class Neckharmonics(Component):

    # https://github.com/wosc/neckharmonics.de/settings/hooks
    # URL: https://neckharmonics.de/_update
    # Content type: json
    # Secret: webhook_token
    # Only push event
    webhook_token = None

    def configure(self):
        self += User('neckharmonics', home='/home/neckharmonics')
        self += File('/home/neckharmonics', ensure='directory',
                     owner='neckharmonics', group='neckharmonics')

        self += File('/etc/nginx/sites-available/neckharmonics.de',
                     source='nginx.conf', is_template=False)
        self += VHost(self._, site_enable=True)

        self += GitClone(
            'https://github.com/wosc/neckharmonics.de',
            target='/home/neckharmonics/public_html',
            owner='neckharmonics')
        for name in ['last.push', 'last.pull']:
            self += MarkerFile(f'/home/neckharmonics/{name}',
                               owner='neckharmonics', mode=0o664)

        self += VirtualEnv(path='/home/neckharmonics/webhook')
        self._ += Requirements(source='requirements.txt')
        self += File('/home/neckharmonics/webhook.py', mode=0o755)

        self += File(
            '/srv/cgiserv/apache.d/neckharmonics.conf',
            source='apache.conf')
        self += CGI(self._)
        # Allow writing to `last.push` marker file via webhook.
        self += GroupMember('neckharmonics', user='cgiserv')

        self += File('/home/neckharmonics/update.sh', mode=0o755)
        self += CronJob(
            self._.path,
            user='neckharmonics',
            timing='* * * * * ')


class GitClone(Component):
    namevar = 'url'
    target = None
    owner = None

    def verify(self):
        if not os.path.exists(f'{self.target}/.git'):
            raise UpdateNeeded()

    def update(self):
        self.cmd(f'git clone {self.url} {self.target}')
        if self.owner:
            self.cmd(f'chown -R {self.owner}: {self.target}')


class MarkerFile(Component):
    namevar = 'path'
    owner = None
    mode = None

    def configure(self):
        self += Presence(self.path)
        self += Mode(self.path, mode=self.mode)
        self += Owner(self.path, owner=self.owner)
        self += Group(self.path, group=self.owner)
