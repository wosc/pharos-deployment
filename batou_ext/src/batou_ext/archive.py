import batou.lib.archive
import os.path
import shutil


class Extract(batou.lib.archive.Extract):

    owner = None
    group = None

    def verify(self):
        if not self.owner and not self.group:
            return
        self.assert_no_subcomponent_changes()

    def update(self):
        for filename in self.extractor.get_names_from_archive():
            filename = os.path.join(*filename.split(os.path.sep)[self.strip:])
            filename = os.path.join(self.target, filename)
            shutil.chown(filename, self.owner, self.group)


def get_names_from_archive(self):
    result = original(self)
    return [x for x in result if os.path.sep in x]


original = batou.lib.archive.Untar.get_names_from_archive
batou.lib.archive.Untar.get_names_from_archive = get_names_from_archive


def zip_get_names(self):
    stdout, stderr = self.cmd(
        'bsdtar tf {{component.archive}}'
    )
    return [x for x in stdout.splitlines() if os.path.sep in x]


batou.lib.archive.Unzip.get_names_from_archive = zip_get_names


def zip_update(self):
    self.cmd(
        'bsdtar xf {{component.archive}} -C {{component.target}} '
        '--strip-components {{component.strip}}'
    )


batou.lib.archive.Unzip.update = zip_update
batou.lib.archive.Unzip._supports_strip = True
