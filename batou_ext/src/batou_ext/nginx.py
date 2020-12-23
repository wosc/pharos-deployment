from batou.component import Component
from batou.lib.file import File
from batou_ext.apt import Package
from batou_ext.file import Delete
import pkg_resources


here = pkg_resources.resource_filename('batou_ext', '') + '/'


class Nginx(Component):

    def configure(self):
        self.provide('nginx', self)
        self += Package('nginx')
        self += Delete('/etc/nginx/sites-enabled/default')
        self += File('/etc/nginx/snippets/ssl.conf', is_template=False,
                     source=here + 'ssl.conf')
        self += File('/etc/nginx/conf.d/gzip.conf', is_template=False,
                     source=here + 'gzip.conf')

    def verify(self):  # Cannot use VHost, since it would create a cycle.
        self.assert_no_subcomponent_changes()

    def update(self):
        self.cmd('systemctl reload nginx')


class VHost(Component):

    namevar = 'dependencies'

    def configure(self):
        self.require_one('nginx', host=self.host)
        if not isinstance(self.dependencies, (list, tuple)):
            self.dependencies = [self.dependencies]

    def verify(self):
        for dependency in self.dependencies:
            dependency.assert_no_changes()

    def update(self):
        self.cmd('systemctl reload nginx')

    @property
    def namevar_for_breadcrumb(self):
        return self.dependencies[0].namevar_for_breadcrumb
