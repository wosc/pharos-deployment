# -*- mode: ruby -*-
# Requirements
# Vagrant >= 2.0
# vagrant plugin install vagrant-lxc --plugin-version 1.2.4
# vagrant plugin install vagrant-berkshelf
# chefdk >= 2.4.17

Vagrant.configure('2') do |config|
  config.vm.box_check_update = false

  config.ssh.forward_agent = true
  config.ssh.shell = 'bash' # https://superuser.com/a/1277604

  config.vm.define 'default' do |default|
    default.vm.hostname = 'cheftest'

    default.vm.provider 'lxc'
    default.vm.box = 'developerinlondon/ubuntu_lxc_xenial_x64'

    default.vm.network "forwarded_port", guest: 80, host: 80

    # Use apt-cacher on host
    default.vm.provision 'shell', inline: 'echo "Acquire::http { Proxy \"http://$(ip route | awk \'/^default/ { print $3 }\'):3142\"; };" > /etc/apt/apt.conf.d/02proxy'
    default.vm.synced_folder '~/install', '/mnt'
    default.vm.provision 'shell', inline: 'if [ ! -x /opt/chef/bin/chef-solo ]; then echo "Installing chef"; dpkg -i /mnt/chef_13.6.4-1_amd64.deb; else echo "chef already installed"; fi'

    default.vm.provision 'chef_zero' do |chef|
      chef.install = false
      chef.log_level = ENV.fetch('CHEF_LOG', 'info').downcase.to_sym
      chef.cookbooks_path = '/home/cache/vagrant-chef' # guaranteed to be empty
      chef.nodes_path = '/home/cache/vagrant-chef' # guaranteed to be empty
      # XXX inline chef.arguments = '--config-option' doesn't work
      chef.custom_config_path = 'client-vagrant.rb'

      # chef.add_recipe 'wosc::packages'
      # chef.add_recipe 'wosc::cron-apt'

      # chef.add_recipe 'wosc-fastcgi'
      # chef.add_recipe 'wosc-letsencrypt'

      # chef.add_recipe 'wosc-mysql'
      # chef.add_recipe 'wosc-mailserver'
      # chef.add_recipe 'wosc-mailserver::mlmmj'
      # chef.add_recipe 'wosc-thyrida'
      # chef.add_recipe 'wosc-roundcube'

      # chef.add_recipe 'wosc-radicale'
      # chef.add_recipe 'wosc-agendav'

      # chef.add_recipe 'wosc-matomo'
      # chef.add_recipe 'wosc-shaarli'
      # chef.add_recipe 'wosc-wallabag'

      # chef.add_recipe 'wosc-prometheus'
      # chef.add_recipe 'wosc-prometheus::exim'
      # chef.add_recipe 'wosc-prometheus::grafana'
      # chef.add_recipe 'wosc-prometheus::mysql'
      # chef.add_recipe 'wosc-prometheus::nginx'
      # chef.add_recipe 'wosc-prometheus::supervisord'

      # chef.add_recipe 'wosc-cgi'
      # chef.add_recipe 'wosc-cgi::ddns'
      # chef.add_recipe 'wosc-cgi::nginxdbauth'
      # chef.add_recipe 'wosc-cgi::passwd'

      # chef.add_recipe 'wosc::pharos'
      # chef.add_recipe 'wosc::woscde'
      # chef.add_recipe 'wosc::controverse'

      # chef.add_recipe 'wosc-wordpress'
      # chef.add_recipe 'wosc::grmusik'

      # chef.add_recipe 'wosc::backup'
      # chef.add_recipe 'wosc::calendar'
      # chef.add_recipe 'wosc::commitmail'
      # chef.add_recipe 'wosc::esniper'
      # chef.add_recipe 'wosc::mail'
      # chef.add_recipe 'wosc::rsspull'
      # chef.add_recipe 'wosc::unison'
      # chef.add_recipe 'wosc::youtube'

      chef.json = {
        "agendav" => {
          "db_pass" => "asdf",
          "csrf_secret" => "ranAcOshab5",
        },
        "ddns" => {
          "user" => "user",
          "pass" => "pass",
          "hostnames" => "example.wosc.de",
        },
        "grmusik" => {
          "db_pass" => "asdf",
          "root_pass" => "asdfasdf",
          "install_wordpress" => true,
        },
        "mailserver" => {
          "db_user" => "mail",
          "db_pass" => "asdf",
          "db_name" => "mailserver",
          "thyrida_root_pass" => "asdfasdf",
        },
        "matomo" => {
          "db_pass" => "asdf",
          "root_pass" => "asdfasdf",
        },
        "prometheus" => {
          "db_pass" => "asdf",
          "root_pass" => "asdfasdf",
        },
        "python" => {
          "pip_version" => "9.0.1",
          "setuptools_version" => "38.4.1",
          "wheel_version" => "0.30.0",
        },
        "roundcube" => {
          "db_pass" => "asdf",
          "store_pass_key" => "UvherdekTatMitVefbuantAl",
        },
        "wallabag" => {
          "db_pass" => "asdf",
          "root_pass" => "asdfasdf",
          "csrf_secret" => "hebPiviatijhiVighEtJerdiConhut",
        },
        "wosc" => {
          "doodle_ical" => "http://example.com"
        }
      }
    end
  end
end
