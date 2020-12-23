from batou.component import Component
from batou.lib.file import File
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User, GroupMember


class Radicale(Component):

    version = '1.1.6'  # XXX Version 2.x removes the "ics-file" storage backend

    def configure(self):
        self += User('radicale')
        self += File('/srv/radicale/data', ensure='directory',
                     owner='radicale', group='radicale')

        deps = []
        self += VirtualEnv(path='/srv/radicale/deployment')
        self._ += Requirements()
        deps.append(self._)

        courier_py = (
            '/srv/radicale/deployment/lib/python%s/site-packages'
            '/radicale/auth/courier.py' % VirtualEnv.version)
        self += Patch(courier_py, source='"GID"', target='b"GID"')
        self += Patch(
            courier_py, source='sock.send(line)',
            target='sock.send(line.encode("utf-8")')
        self += Patch(
            courier_py, source='except Exception:',
            target='except Exception as exception')

        # Allow access to authdaemon
        self += GroupMember('courier', user='radicale')

        for name in ['radicale.conf', 'logging.conf', 'serve.py']:
            self += File('/srv/radicale/%s' % name, is_template=False)
            deps.append(self._)

        self += Program(
            'radicale',
            command='/srv/radicale/deployment/bin/python /srv/radicale/serve.py',
            environ='RADICALE_CONFIG=/srv/radicale/radicale.conf',
            user='radicale',
            dependencies=deps)

        self += File('/srv/radicale/nginx.conf', is_template=False)
        self += VHost(self._)
