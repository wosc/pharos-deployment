include_recipe "wosc-fastcgi::php"
package "php7.0-cli"
package "php7.0-curl"
package "php7.0-gd"
package "php7.0-mbstring"
package "php7.0-mysql"
package "php7.0-xml"
package "php-geoip"
package "geoip-database-contrib"

wosc_service_user "matomo" do
  shell "/bin/bash"
end

group "adm" do  # to read nginx logs
  action :manage
  append true
  members "matomo"
end

VERSION = '3.5.1'

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
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/matomo/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end


package "python2.7"

import_logs = "python2 /srv/matomo/misc/log-analytics/import_logs.py --url https://pharos.wosc.de/logs/ --log-format-name=ncsa_extended --enable-http-errors --enable-http-redirects --enable-static --enable-bots"
cron "import-accesslogs-wosc.de" do
  command "#{import_logs} --idsite=1 /var/log/nginx/wosc.de-access.log.1 > /dev/null"
  hour "8"
  minute "0"
  user "matomo"
  mailto "wosc@wosc.de"
end
cron "import-accesslogs-grmusik.de" do
  command "#{import_logs} --idsite=2 /var/log/nginx/grmusik.de-access.log.1 > /dev/null"
  hour "8"
  minute "30"
  user "matomo"
  mailto "wosc@wosc.de"
end
cron "process-imports" do
  command "php /srv/matomo/console core:archive --url=https://pharos.wosc.de/logs/ > /dev/null"
  hour "9"
  minute "0"
  user "matomo"
  mailto "wosc@wosc.de"
end


file "/etc/sudoers.d/matomo-geoip" do
  content "matomo ALL=(root) NOPASSWD: /usr/sbin/update-geoip-database\n"
end
cron "update-geoip" do
  command "sudo update-geoip-database"
  hour "4"
  minute "45"
  day "15"
  user "matomo"
  mailto "wosc@wosc.de"
end
