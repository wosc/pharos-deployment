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
