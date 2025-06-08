from batou.component import Component
from batou.lib.file import File
from batou_ext.cron import CronJob
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.user import User, GroupMember
import os.path


class LetsEncrypt(Component):

    daemons = ['Debian-exim', 'www-data']
    domains = [
        'grmusik.de',
        'turawa.grmusik.de',
        'wosc.de',
        'mail.wosc.de',
        'pharos.wosc.de',
        'neckharmonics.de',
    ]

    keys = [
        {'target': 'account_key.json', 'source': 'account', 'mode': 0o600},
        {'target': 'account_reg.json', 'source': 'reg', 'mode': 0o600},
        {'target': 'key.pem', 'source': 'key', 'mode': 0o640},
    ]
    # Placeholders for batou secrets
    # Note, account and reg for pharos and wosc.de are the same
    # as mail.wosc.de, and turawa is the same as grmusik.de,
    # but for simplicity it's duplicated here.
    for domain in domains:
        domain = domain.replace('.', '_')
        for name in ['account', 'key', 'reg']:
            locals()[f'{domain}_{name}'] = None
    del domain
    del name

    files = [
        {'target': 'update', 'source': 'update', 'mode': 0o755},
        {'target': 'aliases', 'source': 'aliases', 'mode': 0o600},
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
            content='letsencrypt ALL=(root) NOPASSWD: /usr/bin/systemctl reload nginx, /usr/bin/systemctl reload exim4, /usr/bin/systemctl restart dovecot\n')

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

            for item in self.keys:
                source = '%s.%s' % (domain, item['source'])
                source = source.replace('.', '_')
                self += File(
                    '/srv/letsencrypt/data/%s/%s' % (domain, item['target']),
                    content=getattr(self, source).replace(r'\n', '\n'),
                    is_template=False, mode=item['mode'],
                    owner='letsencrypt', group='letsencrypt')

            for item in self.files:
                if not os.path.exists('%s/data/%s.%s' % (
                        self.defdir, domain, item['source'])):
                    continue
                self += File(
                    '/srv/letsencrypt/data/%s/%s' % (domain, item['target']),
                    source='data/%s.%s' % (domain, item['source']),
                    is_template=False, mode=item['mode'],
                    owner='letsencrypt', group='letsencrypt')
