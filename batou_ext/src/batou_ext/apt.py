from batou import UpdateNeeded
from batou.component import Component
from batou.lib.file import File
import os
import re
import requests


class Package(Component):

    namevar = 'name'
    version = ''
    options = ''

    def verify(self):
        installed = '(none)'
        output, _ = self.cmd('LANG=C apt-cache policy %s' % self.name)
        for line in output.splitlines():
            if 'Installed:' in line:
                installed = line.split()[-1]
                break
        if self.version:
            if installed != self.version:
                raise UpdateNeeded()
        else:
            if installed == '(none)':
                raise UpdateNeeded()

    def update(self):
        version = ''
        if self.version:
            version = '=' + self.version
        self.cmd('apt -y %s install %s%s' % (
            self.options, self.name, version),
            env={'DEBIAN_FRONTEND': 'noninteractive'})


class AptRepository(Component):

    namevar = 'name'
    line = None
    key = None

    def configure(self):
        self += AptKey(self.key, name=self.name)
        self += File('/etc/apt/sources.list.d/%s.list' % self.name,
                     content=self.line)
        self.config = self._

    def verify(self):
        self.config.assert_no_changes()

    def update(self):
        self.cmd('apt update')


class AptKey(Component):

    namevar = 'url'
    name = None

    def configure(self):
        self.key = self.map(self.name) + '.pub'
        self += Download(self.url, target=self.key)

    def verify(self):
        # Adapted from <https://github.com/chef-cookbooks/apt/blob/v5.0.0
        #   /providers/repository.rb#L112-L121>
        installed = self.fingerprints(self.cmd('apt-key finger')[0])
        new = self.fingerprints(self.cmd(
            'gpg --with-subkey-fingerprint %s' % self.key)[0])
        if new - installed:
            raise UpdateNeeded()

    def update(self):
        self.cmd('apt-key add %s' % self.key)

    KEY = re.compile('^ +([0-9A-F ]+)$')  # scary gpg output parsing

    def fingerprints(self, text):
        result = set()
        for line in text.splitlines():
            match = self.KEY.search(line)
            if match:
                result.add(match.group(1).replace(' ', ''))
        return result


class Download(Component):

    namevar = 'url'
    target = None

    def verify(self):
        if not os.path.exists(self.target):
            raise UpdateNeeded()

    def update(self):
        r = requests.get(self.url)
        r.raise_for_status()
        with open(self.target, 'w') as f:
            f.write(r.text)
