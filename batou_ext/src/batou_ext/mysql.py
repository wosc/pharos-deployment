from batou.lib.mysql import Database, User, Grant
from batou.component import Component


class ServiceDatabase(Component):

    namevar = 'database'
    username = None
    password = None
    schema = None

    def configure(self):
        if not self.username:
            self.username = self.database
        if not self.password:
            self.password = self.database
        self += Database(self.database, base_import_file=self.schema)
        self += User(self.username, password=self.password)
        self += Grant(self.database, user=self.username, admin_password=None)
