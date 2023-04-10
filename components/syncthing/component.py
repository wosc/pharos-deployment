from batou.component import Component
from batou.lib.file import File, Directory
from batou_ext.apt import Package
from batou_ext.supervisor import Program


# On clients:
# Set device name
# Disable: Local discovery, Global discovery, Relaying
# Add device pharos, set address to `tcp://pharos.wosc.de:22000`

# Access Server UI via `ssh -NL 8385:localhost:8384 wosc.de` on localhost:8385
# Share Folder with new client


class Syncthing(Component):

    private_key = None

    def configure(self):
        self += Package('syncthing')

        self += Directory('/home/wosc/.config/syncthing')
        self += File('/home/wosc/.config/syncthing/cert.pem',
                     source='cert.pem', is_template=False)
        self += File('/home/wosc/.config/syncthing/key.pem',
                     content=self.private_key.replace(r'\n', '\n'),
                     is_template=False, mode=0o600)

        self += Program(
            'syncthing',
            command='syncthing serve --home=/home/wosc/.config/syncthing',
            environ='HOME=/home/wosc, STNORESTART=1',
            directory='/home/wosc',
            user='wosc')
