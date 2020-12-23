from batou import UpdateNeeded
from batou.component import Component


class GroupMember(Component):

    namevar = 'group'
    user = ''

    def configure(self):
        if not self.group or not self.user:
            raise ValueError('Both group and user is required')

    def verify(self):
        current, _ = self.cmd('id -Gn %s' % self.user)
        current = current.strip().split()
        if self.group not in current:
            raise UpdateNeeded()

    def update(self):
        self.cmd('adduser %s %s' % (self.user, self.group))

    @property
    def namevar_for_breadcrumb(self):
        return '%s -> %s' % (self.user, self.group)
