from batou import UpdateNeeded
from batou.component import Component
import batou.lib.file
import os.path


class Delete(Component):
    """XXX batou.lib.File really should support `ensure=absent`."""

    namevar = 'path'

    def configure(self):
        self.path = self.map(self.path)

    def verify(self):
        if os.path.exists(self.path):
            raise UpdateNeeded()

    def update(self):
        batou.lib.file.ensure_path_nonexistent(self.path)
