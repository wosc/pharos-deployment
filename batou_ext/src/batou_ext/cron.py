from batou import UpdateNeeded
from batou.component import Component, Attribute
from batou.lib.cron import ignore_comments
from batou.lib.file import File
import batou.lib.cron
import collections
import pkg_resources


class CronJob(batou.lib.cron.CronJob):

    key = 'batou_ext.cron:CronJob'
    user = 'root'


class CronTab(Component):

    crontab_template = pkg_resources.resource_filename(
        'batou_ext', 'crontab')
    mailto = ''
    install = Attribute('literal', default='True')

    def configure(self):
        per_user = collections.defaultdict(list)
        for job in self.require(CronJob.key, host=self.host, strict=False):
            per_user[job.user].append(job)

        for user, jobs in per_user.items():
            jobs.sort(key=lambda job: job.command + ' ' + job.args)
            self += File(
                'crontab.%s' % user,
                source=self.crontab_template, template_args={'jobs': jobs})
            if self.install:
                self += InstallCrontab(user, crontab=self._)


class InstallCrontab(Component):

    namevar = 'user'
    crontab = ''

    def verify(self):
        try:
            current, _ = self.cmd(
                'crontab -u %s -l' % self.user, encoding=None)
        except Exception:
            current = ''
        current = ignore_comments(current)
        new = ignore_comments(self.crontab.content)
        if new != current:
            raise UpdateNeeded()

    def update(self):
        self.cmd('crontab -u %s %s' % (self.user, self.crontab.path))
