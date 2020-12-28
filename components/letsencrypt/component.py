from batou.component import Component
from batou.lib.file import File
from batou_ext.cron import CronJob
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.user import User, GroupMember
import os.path


class LetsEncrypt(Component):

    daemons = ['courier', 'Debian-exim', 'www-data']
    domains = [
        'grmusik.de',
        'wosc.de',
        'mail.wosc.de',
        'pharos.wosc.de',
    ]

    files = [
        {'target': 'account_key.json', 'source': '.account', 'mode': 0o600},
        {'target': 'account_reg.json', 'source': '.reg', 'mode': 0o600},
        {'target': 'key.pem', 'source': '.key', 'mode': 0o640},
        {'target': 'update', 'source': '.update', 'mode': 0o755},
        {'target': 'aliases', 'source': '.aliases', 'mode': 0o600},
    ]

    def configure(self):
        self += User('letsencrypt')
        for user in self.daemons:
            self += GroupMember('letsencrypt', user=user)

        self += File('/srv/letsencrypt/public', ensure='directory',
                     owner='letsencrypt', group='letsencrypt')
        self += File('/srv/letsencrypt/data', ensure='directory',
                     owner='letsencrypt', group='letsencrypt', mode=0o770)

        self += VirtualEnv(path='/srv/letsencrypt/deployment')
        self._ += Requirements()

        self += Patch(
            '/srv/letsencrypt/deployment/lib/python%s/site-packages'
            '/simp_le.py' % VirtualEnv.version, target='wosc patched',
            file='logging.patch')

        self += File(
            '/etc/nginx/snippets/letsencrypt.conf',
            source='nginx.conf', is_template=False)

        self += File(
            '/etc/sudoers.d/letsencrypt',
            content='letsencrypt ALL=(root) NOPASSWD: /etc/init.d/nginx, /etc/init.d/exim4, /etc/init.d/courier-imap-ssl\n')

        self += File(
            '/srv/letsencrypt/update-letsencrypt', source='update.sh',
            is_template=False, mode=0o755)

        self += CronJob(
            '/srv/letsencrypt/update-letsencrypt',
            user='letsencrypt',
            timing='15 2 * * *')

        for domain in self.domains:
            self += File(
                '/srv/letsencrypt/public/%s' % domain, ensure='directory',
                owner='letsencrypt', group='letsencrypt')
            self += File(
                '/srv/letsencrypt/data/%s' % domain, ensure='directory',
                owner='letsencrypt', group='letsencrypt')

            for item in self.files:
                if not os.path.exists('%s/data/%s.%s' % (
                        self.defdir, domain, item['source'])):
                    continue
                self += File(
                    '/srv/letsencrypt/data/%s/%s' % (domain, item['target']),
                    source='%s.%s' % (domain, item['source']),
                    is_template=False, mode=item['mode'],
                    owner='letsencrypt', group='letsencrypt')
