from batou import UpdateNeeded
from batou.component import Component, Attribute
import grp
import pwd


class User(Component):

    namevar = 'user'
    shell = '/bin/bash'
    home = Attribute(default='/srv/{{component.user}}')

    def verify(self):
        try:
            pwd.getpwnam(self.user)
        except KeyError:
            raise UpdateNeeded()

    def update(self):
        self.cmd(self.expand(
            'adduser '
            '--home {{component.home}} '
            '--shell {{component.shell}} '
            '{{component.user}}'
        ))


class Group(Component):

    namevar = 'group'

    def verify(self):
        try:
            grp.getgrnam(self.group)
        except KeyError:
            raise UpdateNeeded()

    def update(self):
        self.cmd('addgroup %s' % self.group)


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
