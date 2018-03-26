include_recipe "wosc-fastcgi::php"
package "php7.0-cli"
package "php7.0-curl"
package "php7.0-gd"
package "php7.0-mbstring"
package "php7.0-mysql"
package "php7.0-xml"

wosc_service_user "matomo" do
  shell "/bin/bash"
end

VERSION = '3.3.0'

ark "matomo" do
  url "http://builds.matomo.org/piwik-#{VERSION}.tar.gz"
  action :put
  path "/srv"
  owner "matomo"
  group "matomo"
end

ark "setup" do
  url "https://github.com/nebev/piwik-cli-setup/archive/63fcf3c428ccc1731f94875ac19a11a1640cd63c.zip"
  action :put
  path "/srv/matomo"
  owner "matomo"
  group "matomo"
end

wosc_mysql_database "matomo"
wosc_mysql_user "matomo" do
  password node["matomo"]["db_pass"]
end
wosc_mysql_grant "matomo" do
  user "matomo"
end

template "/srv/matomo/setup/install.json" do
  source "install.json"
  owner "matomo"
  group "matomo"
  mode "0640"
end
execute "php /srv/matomo/setup/install.php" do
  user "matomo"
  not_if "echo 'show tables' | mysql -umatomo -p#{node['matomo']['db_pass']} matomo | grep -q ."
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/matomo.conf" do
  source "supervisor.conf"
  # XXX Too agressive since it restarts *all* services
  # notifies :reload, "service[supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/matomo/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
