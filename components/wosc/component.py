from batou.component import Component
from batou.lib.archive import Extract
from batou.lib.cmmi import Configure, Make
from batou.lib.download import Download
from batou.lib.file import File, Symlink, BinaryFile
from batou_ext.apt import Package
from batou_ext.cron import CronJob
from batou_ext.nginx import VHost
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.user import User, GroupMember
from crypt import crypt
import batou.lib.python


class Backup(Component):

    def configure(self):
        # Used by rsnapshot from laptop
        self += File('/root/.ssh', ensure='directory')
        self += File('/root/.ssh/authorized_keys', source='nautis.pub',
                     is_template=False, mode=0o600)

        # Hourly calendar backup
        self += Package('rsnapshot')
        self += File('/srv/radicale/backup', ensure='directory',
                     owner='radicale', group='radicale')
        self += File('/srv/radicale/backup/wosc.conf',
                     source='rsnapshot-calendar.conf')
        self += CronJob(
            'rsnapshot', args='-c /srv/radicale/backup/wosc.conf hourly',
            user='radicale', timing='0 * * * *')
        self += CronJob(
            'rsnapshot', args='-c /srv/radicale/backup/wosc.conf daily',
            user='radicale', timing='15 0 * * *')

        # Provides access to scheduled todos via my default caldav source
        # XXX This doesn't really belong here, but not worth extracting.
        self += CronJob(
            'curl --silent http://localhost:7078/ical/scheduled > '
            '/srv/radicale/data/wosc@wosc.de/haemera.ics',
            user='wosc',
            timing='*/5 * * * *')


class Controverse(Component):

    def configure(self):
        self += File('/home/controverse', ensure='directory',
                     owner='wosc', group='wosc')

        self += File('/etc/nginx/sites-available/controverse.wosc.de',
                     source='controverse.conf', is_template=False)
        self += VHost(self._, site_enable=True)

        self += File(
            '/etc/exim4/domains/controverse.wosc.de',
            content='mail: "|/usr/bin/mlmmj-recieve -L /var/spool/mlmmj/controverse/"')


class Dailystrips(Component):

    ui_password = None

    def configure(self):
        self += Package('dailystrips')
        self += Patch(
            '/usr/bin/dailystrips',
            target='altpattern',
            file='dailystrips-altpattern.patch', strip=0)

        self += File(
            '/home/wosc/bin/dailycomics.sh', is_template=False, mode=0o755)
        self += CronJob(
            self._.path,
            user='wosc',
            timing='15 5 * * * ')

        self += File('/home/wosc/public_html/dailystrips', ensure='directory',
                     owner='wosc', group='wosc')
        self += BinaryFile(
            '/home/wosc/public_html/dailystrips/favicon.png',
            source='kevinandkell.png', owner='wosc', group='wosc')
        self += File(
            '/home/wosc/public_html/dailystrips/.htpasswd',
            content='wosc:' + crypt(self.ui_password, 'hX'),
            sensitive_data=True)


class WoscDe(Component):

    ds_cookie_secret = None

    def configure(self):
        self += File('/etc/nginx/sites-available/wosc.de',
                     source='wosc.de.conf')
        self += VHost(self._, site_enable=True)


class GRmusik(Component):

    def configure(self):
        self += User(
            'grmusik', home='/home/grmusik',
            shell='/usr/lib/openssh/sftp-server')
        self += File('/etc/nginx/sites-available/grmusik.de',
                     source='grmusik.de.conf', is_template=False)
        self += VHost(self._, site_enable=True)


class RSSPull(Component):

    def configure(self):
        self += VirtualEnv()
        self._ += Requirements(source='rsspull/requirements.txt')

        self += CronJob(
            self.map('bin/rsspull'),
            args='--confdir=/home/wosc/.dot/x11/rsspull',
            user='wosc',
            timing='0 6 * * *')

        # Allow writing directly to Maildir
        self += GroupMember('Debian-exim', user='wosc')

        self += File('logrotate.conf', source='rsspull-logrotate.conf')
        self += CronJob(
            '/usr/sbin/logrotate',
            args=('-s /home/wosc/.dot/x11/rsspull/log.rotate %s/logrotate.conf'
                  % self.workdir),
            user='wosc',
            timing='0 7 * * *')


class ESniper(Component):

    version = "69675c03e17bad51c41a07e1453d897eb8c401af"  # 2.35.0
    checksum = 'sha256:79f4558b23fa43ab2314498e0abb80881cf05fca6dbead8fa054fd2fe6a9b124'

    # XXX This URL only exists after you've clicked on "download snapshot" at
    # https://sourceforge.net/p/esniper/git/ci/{version}/tree/
    url = 'https://sourceforge.net/code-snapshots/git/e/es/esniper/git.git/esniper-git-{version}.zip'

    def configure(self):
        self += Package('libssl-dev')
        self += Package('libcurl4-gnutls-dev')

        self += Download(
            self.url.format(version=self.version), checksum=self.checksum)
        src = self._.target.replace('.zip', '')
        self += Extract(self._.target, create_target_dir=False)

        self += Patch(
            src + '/esniper.c',
            source='#define MIN_BIDTIME 5',
            target='#define MIN_BIDTIME 2')
        self += Configure(src, prefix='/usr/local')
        self += Make(src)


class ArchiveMail(Component):

    password_wosc = ''
    password_grmusik = ''

    def configure(self):
        self += File(
            '/usr/local/bin/archivemail', mode=0o755, is_template=False)

        self += File(
            '/home/wosc/.archivemail-wosc.de', content=self.password_wosc,
            sensitive_data=True, owner='wosc', group='wosc', mode=0o600)
        self += CronJob(
            '/usr/local/bin/archivemail',
            args="--days=14 --delete --output-dir=/tmp "
            "--pwfile /home/wosc/.archivemail-wosc.de "
            "'imaps://wosc@wosc.de#mail.wosc.de/INBOX.copy' > /dev/null",
            user='wosc',
            timing='10 0 * * *')
        self += CronJob(
            '/usr/local/bin/archivemail',
            args="--days=7 --delete --output-dir=/tmp "
            "--pwfile /home/wosc/.archivemail-wosc.de "
            "'imaps://wosc@wosc.de#mail.wosc.de/INBOX.Spam' > /dev/null",
            user='wosc',
            timing='10 0 * * *')

        self += File(
            '/home/grmusik/spam-cleanup.pass', content=self.password_grmusik,
            sensitive_data=True, owner='grmusik', group='grmusik', mode=0o600)
        self += CronJob(
            '/usr/local/bin/archivemail',
            args="--days=1 --delete --output-dir=/tmp "
            "--pwfile /home/grmusik/spam-cleanup.pass "
            "'imaps://gregor@grmusik.de#mail.wosc.de/INBOX.Spam' > /dev/null",
            user='grmusik',
            timing='10 0 * * *')


class Fetchmail(Component):

    packages = [
        'bsd-mailx',
        'fetchmail',
        'mutt',
        't-prot',
        'urlview',
    ]

    def configure(self):
        for name in self.packages:
            self += Package(name)

        self += CronJob(
            "sleep 30; echo `date` | "
            "/usr/bin/mail -s 'pharos rebooted' wosc@localhost",
            user='wosc',
            timing='@reboot')

        self += CronJob(
            'fetchmail',
            args='-f /home/wosc/.dot/mail/fetchmailrc-pharos',
            user='wosc',
            timing='@reboot')


class SSHAuthorizedKeys(Component):

    def configure(self):
        self += File('/home/wosc/.ssh', ensure='directory', owner='wosc', group='wosc')
        self += File('/home/wosc/.ssh/authorized_keys', is_template=False,
                     owner='wosc', group='wosc', mode=0o600)


class YoutubeDL(Component):

    version = '2020.12.14'

    def configure(self):
        self += VirtualEnv()
        self._ += batou.lib.python.Package(
            'youtube-dl', version=self.version, check_package_is_module=False)
        self += Symlink('/usr/local/bin/yt', source=self.map('bin/youtube-dl'))
