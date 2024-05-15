from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.cron import CronJob
from batou_ext.supervisor import Program
from batou_ext.user import GroupMember


# On clients, open localhost:8384
# Set device name
# Disable: Local discovery, Global discovery, Relaying
# Add device pharos (get its ID from pharos UI), set address to `tcp://pharos.wosc.de:22000`

class Syncthing(Component):

    private_key = None

    def configure(self):
        self += Package('syncthing')

        for name in ['sync', 'sync/config', 'tmp']:
            self += File(
                '/home/wosc/%s' % name,
                ensure='directory', owner='wosc', group='wosc')

        self += File('/home/wosc/sync/config/cert.pem', is_template=False)
        self += File('/home/wosc/sync/config/key.pem',
                     content=self.private_key.replace(r'\n', '\n'),
                     is_template=False, mode=0o600)

        # Manually add <user> and <password> to <gui> in sync/config/config.xml
        # passlib.context.CryptContext(schemes=['bcrypt']).hash('mypassword')

        self += Program(
            'syncthing',
            command='syncthing serve --home=/home/wosc/sync/config',
            environ='HOME=/home/wosc, STNORESTART=1',
            directory='/home/wosc',
            user='wosc')

        self += File('/home/wosc/sync/nginx.conf')


class Prom_Syncthing(Component):

    def configure(self):
        # Allow writing to node exporter textfile directory
        self += GroupMember('prometheus', user='wosc')

        self += File('/srv/prometheus/bin/node_exporter-syncthing',
                     source='check_conflict.sh', is_template=False, mode=0o755)
        self += CronJob(
            '/srv/prometheus/bin/node_exporter-syncthing',
            user='wosc',
            timing='7 * * * *')

        self += File(
            '/srv/prometheus/conf.d/alert-syncthing.yml',
            source='alert.yml', is_template=False)
        self.provide('prom:rule', self._)
