from batou.component import Component
from batou.lib.archive import Extract
from batou.lib.cmmi import Configure, Make
from batou.lib.download import Download
from batou.lib.file import File, Symlink
from batou_ext.apt import Package
from batou_ext.cron import CronJob
from batou_ext.patch import Patch
from batou_ext.python import VirtualEnv, Requirements


class RSSPull(Component):

    def configure(self):
        self += VirtualEnv()
        self += Requirements('rsspull.txt')
        self += Symlink(
            '/usr/local/bin/rsspull', source=self.map('bin/rsspull'))

        self += CronJob(
            '/usr/local/bin/rsspull',
            args='--confdir=/home/wosc/.dot/x11/rsspull',
            user='wosc',
            timing='0 6 * * *')
        self += CronJob(
            '/usr/local/bin/rsspull',
            args='--confdir=/home/wosc/.dot/x11/rsspull-kolumbus',
            user='wosc',
            timing='0 6 * * *')

        # TODO: Add wosc to group Debian-exim


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
        self += Package('archivemail')
        self += Patch(
            '/usr/bin/archivemail', file='archivemail-username.patch',
            target='wosc patched')

        self += File(
            '/home/wosc/.archivemail-wosc.de', content=self.password_wosc,
            sensitive_data=True, owner='wosc', group='wosc', mode=0o600)
        self += CronJob(
            'archivemail',
            args="--days=14 --delete --output-dir=/tmp "
            "--pwfile /home/wosc/.archivemail-wosc.de "
            "'imaps://wosc@wosc.de#mail.wosc.de/INBOX.copy' > /dev/null",
            user='wosc',
            timing='10 0 * * *')
        self += CronJob(
            'archivemail',
            args="--days=7 --delete --output-dir=/tmp "
            "--pwfile /home/wosc/.archivemail-wosc.de "
            "'imaps://wosc@wosc.de#mail.wosc.de/INBOX.Spam' > /dev/null",
            user='wosc',
            timing='10 0 * * *')

        self += File(
            '/home/grmusik/spam-cleanup.pass', content=self.password_wosc,
            sensitive_data=True, owner='grmusik', group='grmusik', mode=0o600)
        self += CronJob(
            'archivemail',
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
