from batou.component import Component
from batou.lib.file import File
from batou.lib.python import Package
import batou.lib.python


class VirtualEnv(batou.lib.python.VirtualEnv):

    version = '3.6'

    bootstrap_versions = {
        'pip': '20.1.1',
        'setuptools': '47.3.1',
        'wheel': '0.34.2',
    }

    def __init__(self, namevar=None, **kw):
        if namevar is None:
            namevar = self.version
        super().__init__(namevar=namevar, **kw)

    def configure(self):
        super().configure()
        for package, version in self.bootstrap_versions.items():
            self += Package(package, version=version)


class Requirements(Component):

    namevar = 'filename'
    filename = 'requirements.txt'
    success_marker = '.batou.pip.success'

    def configure(self):
        self += File(self.filename)
        self.requirements = self._.path
        self.dependencies = [self.requirements]

    def verify(self):
        self.assert_file_is_current(self.success_marker, self.dependencies)

    def update(self):
        self.cmd('bin/pip install --no-deps -r %s' % self.requirements)
        self.cmd('bin/pip check')
        self.touch(self.success_marker)
