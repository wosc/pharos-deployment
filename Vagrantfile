# -*- mode: ruby -*-
# Requirements
# Vagrant >= 2.0
# vagrant plugin install vagrant-lxc

Vagrant.configure('2') do |config|
  config.vm.box_check_update = false

  config.ssh.forward_agent = true
  config.ssh.shell = 'bash' # https://superuser.com/questions/1160025

  config.vm.define 'batou-pharos' do |default|
    default.vm.hostname = 'batou-pharos'

    default.vm.provider 'lxc'
    default.vm.box = 'zeitonline/bionic64-lxc'

    # default.vm.network "forwarded_port", guest: 80, host: 80

    # https://superuser.com/questions/1160025 continued for batou
    default.vm.provision 'shell', inline: 'sed -i -e "s/^mesg n.*$/tty -s \&\& mesg n/" /root/.profile'
    # Use apt-cacher on host
    default.vm.provision 'shell', inline: 'echo "Acquire::http { Proxy \"http://$(ip route | awk \'/^default/ { print $3 }\'):3142\"; };" > /etc/apt/apt.conf.d/02proxy'
    # Use devpi on host
    default.vm.provision 'shell', inline: 'mkdir /root/.pip; export HOST=$(ip route | awk \'/^default/ { print $3 }\'); echo -e "[global]\nindex-url=http://$HOST:4040/root/pypi/+simple/\ntrusted-host=$HOST" > /root/.pip/pip.conf'
    # Un-break python on debian
    default.vm.provision 'shell', inline: 'export DEBIAN_FRONTEND=noninteractive; apt update; apt -y install python3-venv'
  end
end
