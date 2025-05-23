from batou import UpdateNeeded
from batou.component import Component
from batou.lib.cmmi import Build
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.mysql import ServiceDatabase
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.systemd import Service
from batou_ext.user import User, GroupMember
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
        self += Dovecot(
            db_name=self.db_name,
            db_username=self.db_username,
            db_password=self.db_password)
        self += Auth(
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
        'spamd',
        'spamc',
        'libdbi-perl',
        'libdbd-mysql-perl',
        'pyzor',
        'razor',
        'unbound',
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += File(
            '/etc/unbound/unbound.conf.d/listen.conf',
            source='spam/unbound.conf', is_template=False)
        self += Service('unbound', deps=[self._])

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
        self += File('/etc/default/spamd', source='spam/default',
                     is_template=False)
        deps.append(self._)
        self += Patch(
            '/etc/spamassassin/v310.pre',
            source='#loadplugin Mail::SpamAssassin::Plugin::DCC',
            target='loadplugin Mail::SpamAssassin::Plugin::DCC',
            check_source_removed=True)
        deps.append(self._)
        self += Service('spamd', action='restart', deps=deps)

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


class Dovecot(Component):

    db_name = None
    db_username = None
    db_password = None

    def configure(self):
        self += Package('dovecot-imapd')
        self += Package('dovecot-mysql')

        deps = []
        self += File('/etc/dovecot/dovecot.conf', is_template=False)
        deps.append(self._)
        self += File('/etc/dovecot/dovecot-sql.conf.ext', mode=0o660)
        deps.append(self._)
        self += Service('dovecot', deps=deps)


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


class Auth(Component):

    db_name = None
    db_username = None
    db_password = None

    instances = {
        'mailbox': 7071,
        'mailui': 7072,
    }

    def configure(self):
        self += User('mailauth')

        self += VirtualEnv(path='/srv/mailauth/deployment')
        self._ += Requirements(source='auth/requirements.txt')
        req = self._

        for name, port in self.instances.items():
            self += File(
                f'/srv/mailauth/{name}.conf',
                source=f'auth/{name}.conf',
                owner='mailauth', group='mailauth', mode=0o640)
            config = self._

            self += Program(
                f'auth-{name}',
                command='/srv/mailauth/deployment/bin/nginx-db-auth-serve '
                f'--host localhost --port {port} '
                f'--config /srv/mailauth/{name}.conf',
                user='mailauth',
                dependencies=[req, config]
            )

        self += File(
            '/srv/mailauth/nginx.conf',
            source='auth/nginx.conf', is_template=False)
        self += VHost(self._)
