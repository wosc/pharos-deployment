from batou.lib.mysql import Database, User, Grant
from batou.component import Component


class ServiceDatabase(Component):

    namevar = 'database'
    username = None
    password = None

    def configure(self):
        if not self.username:
            self.username = self.database
        if not self.password:
            self.password = self.database
        self += Database(self.database)
        self += User(self.username, password=self.password)
        self += Grant(self.database, user=self.username, admin_password=None)
