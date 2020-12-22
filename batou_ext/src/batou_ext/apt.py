from batou import UpdateNeeded
from batou.component import Component


class Package(Component):

    namevar = 'name'
    version = ''
    options = ''

    def verify(self):
        output, _ = self.cmd('LANG=C apt-cache policy %s' % self.name)
        for line in output.splitlines():
            if 'Installed:' in line:
                break
        installed = line.split()[-1]
        if self.version:
            if installed != self.version:
                raise UpdateNeeded()
        else:
            if installed == '(none)':
                raise UpdateNeeded()

    def update(self):
        version = ''
        if self.version:
            version = '=' + self.version
        self.cmd('apt -y %s install %s%s' % (
            self.options, self.name, version),
            env={'DEBIAN_FRONTEND': 'noninteractive'})
