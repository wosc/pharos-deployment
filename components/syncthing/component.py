from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.supervisor import Program


# On clients:
# Set device name
# Disable: Local discovery, Global discovery, Relaying
# Add device pharos, set address to `tcp://pharos.wosc.de:22000`

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
