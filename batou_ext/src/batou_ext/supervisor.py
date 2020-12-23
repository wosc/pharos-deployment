from batou import UpdateNeeded
from batou.component import Component, Attribute
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.user import Group
import pkg_resources


here = pkg_resources.resource_filename('batou_ext', '') + '/'


class Supervisor(Component):

    def configure(self):
        self.provide('supervisor', self)

        self += Package('supervisor')
        self += Symlink('/usr/local/bin/sv', source='/usr/bin/supervisorctl')
        self += File(
            '/usr/lib/tmpfiles.d/supervisor.conf',
            content='# Generated by batou\nd /var/run/supervisor 0755 root root')
        self += Group('supervisor')

        self += File('/etc/supervisor/supervisord.conf', is_template=False,
                     source=here + 'supervisord.conf')

    def verify(self):
        self.assert_no_subcomponent_changes()

    def update(self):
        self.cmd('systemctl restart supervisor')


class Program(Component):

    namevar = 'name'

    command = None
    user = 'root'

    autorestart = 'true'
    redirect_stderr = 'true'
    stdout_logfile = '/var/log/supervisor/%(program_name)s.log'

    option_names = [
        'command', 'user',
        'autorestart', 'redirect_stderr', 'stdout_logfile',
    ]

    dependencies = None

    def configure(self):
        if not self.command:
            raise ValueError('command is required')

        self.require_one('supervisor', host=self.host)
        if self.dependencies is None:
            self.dependencies = (self.parent,)

        self += File('/etc/supervisor/conf.d/%s.conf' % self.name,
                     source=here + 'program.conf')

    @property
    def options(self):
        for key in self.option_names:
            value = getattr(self, key)
            if value:
                yield key, value

    def ctl(self, args, **kw):
        return self.cmd('supervisorctl %s' % args, **kw)

    def is_running(self):
        out, _ = self.ctl('status %s' % self.name, ignore_returncode=True)
        return 'RUNNING' in out

    def verify(self):
        for dependency in self.dependencies:
            dependency.assert_no_changes()
        running = self.is_running()
        if not running:
            raise UpdateNeeded()

    def update(self):
        self.ctl('reread')
        self.ctl('update')
        self.ctl('restart %s' % self.name)
        # XXX wait for running?


class PHP(Program):

    command = '/usr/bin/php-cgi -d error_log=/dev/stderr'
    params = None

    socket = 'unix:///run/supervisor/%(program_name)s.sock'
    socket_owner = Attribute(default='{{component.user}}:www-data')
    socket_mode = '0770'

    option_names = Program.option_names + [
        'socket', 'socket_owner', 'socket_mode'
    ]

    dependencies = ()

    def configure(self):
        if self.params:
            for key, value in self.params.items():
                self.command += ' -d %s=%s' % (key, value)
        super().configure()
