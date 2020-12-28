from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User


class Tabu(Component):

    def configure(self):
        self += User('tabu')

        self += VirtualEnv(path='/srv/tabu/deployment')
        self._ += Requirements(source='tabu.txt')

        self += Program(
            'tabu',
            command='/srv/tabu/deployment/bin/tabu-serve 7080',
            user='tabu',
            dependencies=[self._, self._.parent])

        self += File(
            '/srv/tabu/nginx.conf', source='tabu.conf', is_template=False)
        self += VHost(self._)


class Roborally(Component):

    def configure(self):
        self += Package('mongodb')
        self += User('robometeor')

        # meteor build dist
        # scp dist/robometeor.tar.gz wosc.de:/srv/robometeor
        # tar xf /srv/robometeor/robometeor.tar.gz
        # cd bundle/programs/server && npm install

        # replace in programs/web.browser/12345.js:
        # `Router.route('/` with `Router.router('/roborally/`
        # prefix with `/roborally`:
        # `/robots/`, `/tiles/`, `/finish.png`, `/start.png`,
        # `/damage-token.png`, `/Power_Off.png`

        self += Program(
            'robometeor',
            command='node /srv/robometeor/bundle/main.js',
            environ='BIND_IP=127.0.0.1, PORT=7082, '
            'ROOT_URL=https://wosc.de/roborally, '
            'MONGO_URL=mongodb://localhost:27017/robometeor',
            user='robometeor',
            dependencies=())

        self += File(
            '/srv/robometeor/nginx.conf', source='roborally.conf',
            is_template=False)
        self += VHost(self._)
