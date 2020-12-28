from batou import UpdateNeeded
from batou.component import Component, Attribute
import os.path
import re


class Patch(Component):

    namevar = 'path'
    path = Attribute()

    # inline
    source = ''
    target = ''
    check_source_removed = False  # useful when only removing comments

    # separate file
    file = ''
    strip = '0'

    def configure(self):
        if self.source and self.file:
            raise ValueError('Either source or file must be given')
        if not self.target:
            raise ValueError('Target text is required')

    def verify(self):
        if not os.path.exists(self.path):
            return
        file = open(self.path).read()
        if self.check_source_removed and self.source in file:
            raise UpdateNeeded()
        elif self.target not in file:
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
            self.cmd('patch -d/ -p%s < %s/%s' % (
                self.strip, self.parent.defdir, self.file))
