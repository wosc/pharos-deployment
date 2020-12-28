from batou.lib.mysql import Command, Database, Grant
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


class User(Component):
    """Copy&paste to remove `PASSWORD()` function call, which does not exist in
    mysql-8.0 anymore."""

    namevar = "user"
    password = None
    allow_from_hostname = "localhost"
    admin_password = None

    def configure(self):

        create = self.expand("""\
CREATE USER '{{component.user}}'@'{{component.allow_from_hostname}}';
""")
        create_unless = self.expand("""\
SELECT *
FROM user
WHERE
    User = '{{component.user}}'
    AND
    Host = '{{component.allow_from_hostname}}';
""")
        self += Command(
            create, unless=create_unless, admin_password=self.admin_password)

        set_password = self.expand("""\
SET PASSWORD FOR
    '{{component.user}}'@'{{component.allow_from_hostname}}' =
    '{{component.password}}';
""")
        self += Command(set_password, admin_password=self.admin_password)
