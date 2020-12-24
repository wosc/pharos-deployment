from batou.component import Component
from batou.lib.file import File
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
