from batou import UpdateNeeded
from batou.component import Component, Attribute
from batou.lib.file import File
import re


class Patch(Component):

    namevar = 'path'
    path = Attribute()

    # inline
    source = ''
    target = ''

    # separate file
    file = ''
    strip = '0'

    def configure(self):
        if self.source and self.file:
            raise ValueError('Either source or file must be given')
        if not self.target:
            raise ValueError('Target text is required')

        if self.file:
            self += File(self.file, is_template=False)
            self.file = self._

    def verify(self):
        if self.target not in open(self.path).read():
            raise UpdateNeeded()

    def update(self):
        if self.source:
            with open(self.path) as f:
                contents = f.read()
            contents = re.sub(
                self.source, self.target, contents, flags=re.MULTILINE)
            with open(self.path, 'w') as f:
                f.write(contents)
        else:
            self.cmd('patch -d/ -p%s < %s' % (self.strip, self.file.path))
