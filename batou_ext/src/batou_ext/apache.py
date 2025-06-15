from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.nginx import VHost
from batou_ext.supervisor import Program
from batou_ext.user import User
import os.path


here = os.path.dirname(__file__) + '/'


class CGIServer(Component):

    def configure(self):
        self.provide('apache', self)
        self += Package('apache2')

        self += User('cgiserv')
        for name in ['apache.d', 'nginx.d']:
            self += File('/srv/cgiserv/%s' % name, ensure='directory')

        self += File(
            '/srv/cgiserv/apache.conf', owner='cgiserv', group='cgiserv',
            source=here + 'apache.conf', is_template=False)
        self += Program(
            'cgiserv',
            command='/usr/sbin/apache2 -d /usr/lib/apache2 '
                    '-f /srv/cgiserv/apache.conf -k start -X',
            user='cgiserv',
            dependencies=[self._])

        self += File(
            '/srv/cgiserv/nginx.conf',
            source=here + 'cgi.conf', is_template=False)
        self += VHost(self._)

    def verify(self):
        self.assert_no_subcomponent_changes()

    def update(self):
        self.cmd('systemctl disable apache2')
        self.cmd('systemctl disable apache-htcacheclean')


class CGI(Component):

    namevar = 'dependencies'

    def configure(self):
        self.require_one('apache', host=self.host)
        if not isinstance(self.dependencies, (list, tuple)):
            self.dependencies = [self.dependencies]

    def verify(self):
        for dependency in self.dependencies:
            dependency.assert_no_changes()

    def update(self):
        self.cmd('supervisorctl restart cgiserv')

    @property
    def namevar_for_breadcrumb(self):
        return self.dependencies[0].namevar_for_breadcrumb
