from batou.component import Component
from batou.lib.file import File
from batou.lib.git import Clone
from batou_ext.apt import AptRepository, Package
from batou_ext.nginx import VHost
from batou_ext.python import VirtualEnv, Requirements
from batou_ext.supervisor import Program
from batou_ext.user import User


class Tabu(Component):

    def configure(self):
        self += User('tabu')

        self += VirtualEnv(path='/srv/tabu/deployment')
        self._ += Requirements(source='tabu.txt')

        self += Program(
            'tabu',
            command='/srv/tabu/deployment/bin/tabu-serve 7080',
            user='tabu',
            dependencies=[self._, self._.parent])

        self += File(
            '/srv/tabu/nginx.conf', source='tabu.conf', is_template=False)
        self += VHost(self._)


class Roborally(Component):

    def configure(self):
        distro, _ = self.cmd('lsb_release -s -c')
        distro = distro.strip()
        self += Package('apt-transport-https')
        self += AptRepository(
            'mongodb',
            url='https://repo.mongodb.org/apt/ubuntu',
            distro='%s/mongodb-org/8.0' % distro,
            component='multiverse',
            key='https://www.mongodb.org/static/pgp/server-8.0.asc')

        self += Package('mongodb-org')
        self += User('robometeor')

        # Download URL taken from https://github.com/meteor/meteor/blob/release/METEOR@3.1/npm-packages/meteor-installer/install.js#L94-L95
        # wget https://static.meteor.com/packages-bootstrap/3.1/meteor-bootstrap-os.linux.x86_64.tar.gz
        # mkdir /opt/meteor
        # tar xf; mv .meteor/* /opt/meteor
        # add `export METEOR_WAREHOUSE_DIR=/opt/meteor` to `/opt/meteor/meteor`

        # meteor build dist
        # scp dist/robometeor.tar.gz wosc.de:/srv/robometeor
        # rm -rf /srv/robometeor/bundle/*; tar xfC robometeor.tar.gz /srv/robometeor/; npm install --prefix /srv/robometeor/bundle/programs/server; sudo chmod -R a+r /srv/robometeor/bundle; sudo sv restart robometeor

        # replace in programs/web.browser/12345.js:
        # `Router.route("/` with `Router.router("/roborally/`
        # prefix with `/roborally`:
        # `/robots/`, `/tiles/`, `/finish.png`, `/start.png`,
        # `/damage-token.png`, `/Power_Off.png`

        self += Program(
            'robometeor',
            command='node /srv/robometeor/bundle/main.js',
            environ='BIND_IP=127.0.0.1, PORT=7082, '
            'ROOT_URL=https://wosc.de/roborally, '
            'MONGO_URL=mongodb://localhost:27017/robometeor',
            user='robometeor',
            dependencies=())

        self += File(
            '/srv/robometeor/nginx.conf', source='roborally.conf',
            is_template=False)
        self += VHost(self._)


class Seanopoly(Component):

    def configure(self):
        self += User('seanopoly')

        self += Clone(
            'https://github.com/wosc/monopoly', branch='master',
            target='/srv/seanopoly/app')
        git = self._
        app = git.target + '/game'
        self += NPM(app)
        self += NPM(
            app + '/client', commands=['install --no-save', 'run build'],
            dependencies=git)

        # The app wants to write logs here.
        self += File(app + '/static', ensure='directory',
                     owner='seanopoly', group='seanopoly')

        self += Program(
            'seanopoly',
            command='node %s/server/server.js' % app,
            directory=app,
            environ='HTTP=true, BIND=127.0.0.1, PORT=7083, VHOST_PATH=/seanopoly',
            user='seanopoly')

        self += File(
            '/srv/seanopoly/nginx.conf', source='seanopoly.conf',
            is_template=False)
        self += VHost(self._)


class NPM(Component):

    namevar = 'target'
    commands = ['install --no-save']
    dependencies = ()

    def configure(self):
        self.success_marker = '%s/.batou.npm.success' % self.target
        if not isinstance(self.dependencies, (list, tuple)):
            self.dependencies = [self.dependencies]

    def verify(self):
        self.assert_file_is_current(self.success_marker, [
            self.target + '/package.json',
            self.target + '/package-lock.json'])
        for dependency in self.dependencies:
            dependency.assert_no_changes()

    def update(self):
        with self.chdir(self.target):
            for command in self.commands:
                self.cmd('npm %s' % command)
        self.touch(self.success_marker)
