from batou.component import Component
from batou.lib.file import File
from batou.lib.python import Package
import batou.lib.python


class VirtualEnv(batou.lib.python.VirtualEnv):

    version = '3.10'
    path = None

    bootstrap_versions = {
        'pip': '22.3',
        'setuptools': '65.5.0',
        'wheel': '0.37.1',
    }

    def __init__(self, namevar=None, **kw):
        if namevar is None:
            namevar = self.version
        super().__init__(namevar=namevar, **kw)

    def configure(self):
        if self.path:
            self.workdir = self.map(self.path)
        super().configure()
        for package, version in self.bootstrap_versions.items():
            self += Package(package, version=version)


class Requirements(Component):

    namevar = 'filename'
    filename = 'requirements.txt'
    source = None
    success_marker = '.batou.pip.success'

    def __init__(self, namevar=None, **kw):
        if namevar is None:
            namevar = self.filename
        super().__init__(namevar=namevar, **kw)

    def configure(self):
        if not isinstance(self.parent, VirtualEnv):
            raise TypeError('Requirements must be added to a VirtualEnv')
        if self.parent.path:
            self.workdir = self.map(self.parent.path)

        self += File(self.filename, source=self.source)
        self.requirements = self._.path
        self.dependencies = [self.requirements]

    def verify(self):
        self.assert_file_is_current(self.success_marker, self.dependencies)

    def update(self):
        self.cmd('bin/pip install --no-deps -r %s' % self.requirements)
        self.cmd('bin/pip check')
        self.touch(self.success_marker)
