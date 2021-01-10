from batou.component import Component


class Service(Component):

    namevar = 'service'
    action = 'reload'
    deps = ()

    def configure(self):
        if not isinstance(self.deps, (list, tuple)):
            self.deps = [self.deps]

    def verify(self):
        for dependency in self.deps:
            dependency.assert_no_changes()

    def update(self):
        self.cmd('systemctl %s %s' % (self.action, self.service))

    @property
    def namevar_for_breadcrumb(self):
        return '%s %s' % (self.action, self.service)


class SystemdConfig(Component):

    namevar = 'dependencies'

    def configure(self):
        if not isinstance(self.dependencies, (list, tuple)):
            self.dependencies = [self.dependencies]

    def verify(self):
        for dependency in self.dependencies:
            dependency.assert_no_changes()

    def update(self):
        self.cmd('systemctl daemon-reload')

    @property
    def namevar_for_breadcrumb(self):
        return self.dependencies[0].namevar_for_breadcrumb
