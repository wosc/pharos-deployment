from batou import UpdateNeeded
from batou.component import Component
from batou.lib.cmmi import Build
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.mysql import ServiceDatabase
from batou_ext.patch import Patch
from batou_ext.systemd import Service
from batou_ext.user import GroupMember
import os.path
import pwd


class Mailserver(Component):

    db_name = 'mailserver'
    db_username = 'mail'
    db_password = None
    thyrida_root_password = None

    def configure(self):
        # XXX
        # pwd_context = passlib.context.CryptContext(schemes=['bcrypt'])
        # self.thyrida_root_password = pwd_context.hash(self.thyrida_root_password)
        self += Exim(
            db_name=self.db_name,
            db_username=self.db_username,
            db_password=self.db_password,
            thyrida_root_password=self.thyrida_root_password)
        self += Clamav()
        self += SpamAssassin(
            db_name=self.db_name,
            db_username=self.db_username,
            db_password=self.db_password)
        self += Courier(
            db_name=self.db_name,
            db_username=self.db_username,
            db_password=self.db_password)


class Exim(Component):

    # XXX Having to repeat/pass-through these settings is annoying.
    db_name = None
    db_username = None
    db_password = None
    thyrida_root_password = None

    def configure(self):
        self += Package('exim4-daemon-heavy')

        if self.exim_user:  # Handle case "package is not installed yet"
            self += File('/etc/exim4/schema.sql')
            schema = self._
            self += ServiceDatabase(
                self.db_name,
                username=self.db_username, password=self.db_password,
                schema=schema.path)
            self += Service('exim4', action='restart', deps=schema)

        self += DisableDebconf()

        self += File('/etc/exim4/domains', ensure='directory')

        self += Symlink(
            '/etc/exim4/system-filter',
            source='/home/wosc/.dot/mail/.filter-system')
        if os.path.exists('/var/mail/wosc@wosc.de'):
            self += Symlink('/var/mail/wosc@wosc.de/filter',
                            source='/home/wosc/.dot/mail/.filter')

        self += File('/etc/aliases', is_template=False)
        self += File('/etc/email-addresses', content='wosc: wosc@wosc.de')

        self += File('/etc/default/exim4', source='exim4.default',
                     is_template=False)
        self += Service('exim4', action='restart', deps=self._)
        self += File('/etc/exim4/exim4.conf')
        self += Service('exim4', action='reload', deps=self._)

        self += File('/var/mail', ensure='directory', group='Debian-exim')

    @property
    def exim_user(self):
        try:
            user = pwd.getpwnam('Debian-exim')
            return {'uid': user.pw_uid, 'gid': user.pw_gid}
        except KeyError:
            return None


class Clamav(Component):

    def configure(self):
        self += Package('clamav')
        self += Package('clamav-daemon')
        self += GroupMember('clamav', user='Debian-exim')
        self += File('/var/spool/exim4/scan', ensure='directory',
                     owner='Debian-exim', group='clamav')


class SpamAssassin(Component):

    db_name = None
    db_username = None
    db_password = None

    packages = [
        'spamassassin',
        'spamc',
        'libdbi-perl',
        'libdbd-mysql-perl',
        'pyzor',
        'razor',
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += SASchema(
            'sa_pref', db_name=self.db_name,
            command="sed -e 's/userpref/sa_pref/' "
            "-e 's/TYPE=MyISAM/ENGINE=InnoDB/' "
            "/usr/share/doc/spamassassin/sql/userpref_mysql.sql")
        self += SASchema(
            'bayes_vars', db_name=self.db_name,
            command='cat /usr/share/doc/spamassassin/sql/bayes_mysql.sql')
        # self += SASchema(
        #     'sa_txrep', db_name=self.db_name,
        #     command="sed -e 's/txrep/sa_txrep/' "
        #     "/usr/share/doc/spamassassin/sql/txrep_mysql.sql")

        deps = []
        self += File('/etc/spamassassin/local.cf', source='spam/local.conf')
        deps.append(self._)
        self += File('/etc/default/spamassassin', source='spam/default',
                     is_template=False)
        deps.append(self._)
        self += Patch(
            '/etc/spamassassin/v310.pre',
            source='#loadplugin Mail::SpamAssassin::Plugin::DCC',
            target='loadplugin Mail::SpamAssassin::Plugin::DCC',
            check_source_removed=True)
        deps.append(self._)
        self += Service('spamassassin', action='restart', deps=deps)

        self += File('/etc/spamassassin/pyzor', ensure='directory')
        self += File('/etc/spamassassin/pyzor/servers',
                     content='public.pyzor.org:24441')

        self += File(
            '/usr/lib/tmpfiles.d/spamassassin.conf',
            content='# Generated by batou\nd /run/spamassassin 0755 nobody nogroup')

        for name in ['clean', 'learn']:  # unused: awl
            self += File(
                '/etc/cron.daily/spam-%s' % name, mode=0o755,
                source='spam/%s.sh' % name, is_template=False)


class SASchema(Component):

    namevar = 'table'
    db_name = None
    command = None

    def verify(self):
        out, _ = self.cmd(
            'echo "show tables" | mysql -uroot %s' % self.db_name)
        if self.table not in out:
            raise UpdateNeeded()

    def update(self):
        self.cmd('%s | mysql -Bs -uroot %s' % (self.command, self.db_name))


class Courier(Component):

    db_name = None
    db_username = None
    db_password = None

    def configure(self):
        self += Package('courier-imap')
        self += Package('courier-authlib-mysql')
        self += Package('gamin')
        self += GroupMember('courier', user='Debian-exim')

        deps = []
        self += File(
            '/etc/courier/authdaemonrc', source='courier/authdaemonrc',
            owner='daemon', group='daemon', mode=0o660, is_template=False)
        deps.append(self._)
        self += File(
            '/etc/courier/authmysqlrc', source='courier/authmysqlrc',
            owner='daemon', group='daemon', mode=0o660)
        deps.append(self._)
        self += Service('courier-authdaemon', action='restart', deps=deps)

        self += File('/etc/courier/imapd-ssl', source='courier/imapd-ssl',
                     is_template=False)
        self += Service('courier-imap-ssl', action='restart', deps=self._)

        self += Package('socat')
        self += File('/usr/local/bin/authdaemon-test', mode=0o755,
                     source='courier/authdaemon-test', is_template=False)


class DisableDebconf(Component):

    def configure(self):
        self += File('/etc/exim4/update-exim4.conf',
                     content="dc_eximconfig_configtype='none'")

    def verify(self):
        self.assert_no_subcomponent_changes()

    def update(self):
        self.cmd('update-exim4.conf')


class MLMMJ(Component):

    def configure(self):
        self += Package('mlmmj')

        self += Package('bison')
        self += Build(
            'http://www.hypermail-project.org/hypermail-2.3.0.tar.gz',
            checksum='sha256:619938b0cf54eae786f36ef237f106ef7bff7a5c69904ca32afd8d47bf1605d1',
            prefix='/usr/local')

        self += File(
            '/usr/local/bin/mlmmj-update-archives', mode=0o755,
            source='mlmmj/update-archives.sh', is_template=False)
        self += File('/etc/cron.d/mlmmj', source='mlmmj/cron')
