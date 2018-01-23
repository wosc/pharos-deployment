# -*- mode: ruby -*-
# Requirements
# Vagrant >= 2.0
# vagrant plugin install vagrant-lxc --plugin-version 1.2.4
# chefdk >= 2.4.17

Vagrant.configure('2') do |config|
  config.vm.box_check_update = false

  config.ssh.forward_agent = true
  config.ssh.shell = 'bash' # https://superuser.com/a/1277604

  config.vm.define 'default' do |default|
    default.vm.hostname = 'cheftest'

    default.vm.provider 'lxc'
    default.vm.box = 'developerinlondon/ubuntu_lxc_xenial_x64'

    # Use apt-cacher on host
    default.vm.provision 'shell', inline: 'echo "Acquire::http { Proxy \"http://$(ip route | awk \'/^default/ { print $3 }\'):3142\"; };" > /etc/apt/apt.conf.d/02proxy'
    default.vm.synced_folder '~/install', '/mnt'
    default.vm.provision 'shell', inline: 'if [ ! -x /opt/chef/bin/chef-solo ]; then echo "Installing chef"; dpkg -i /mnt/chef_13.6.4-1_amd64.deb; else echo "chef already installed"; fi'

    default.vm.provision 'chef_zero' do |chef|
      chef.install = false
      chef.log_level = ENV.fetch('CHEF_LOG', 'info').downcase.to_sym
      chef.nodes_path = '/home/cache/vagrant-chef' # guaranteed to be empty

      chef.add_recipe 'wosc-radicale'

      chef.json = {
      }
    end
  end
end
