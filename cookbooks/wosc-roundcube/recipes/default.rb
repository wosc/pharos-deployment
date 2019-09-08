include_recipe "wosc-fastcgi::php"
package "php7.2-intl"
package "php7.2-json"
package "php7.2-mbstring"
package "php7.2-mysql"
package "php7.2-xml"

wosc_service_user "roundcube" do
  shell "/bin/bash"
end

VERSION = '1.3.10'

ark "roundcube" do
  url "https://github.com/roundcube/roundcubemail/releases/download/#{VERSION}/roundcubemail-#{VERSION}-complete.tar.gz"
  action :put
  path "/srv"
  owner "roundcube"
  group "roundcube"
end

directory "/srv/roundcube/installer" do
  action :delete
  recursive true
end

template "/srv/roundcube/config/config.inc.php" do
  source "config.php"
  owner "roundcube"
  group "roundcube"
  mode "0640"
end

wosc_mysql_database "roundcube"
wosc_mysql_user "roundcube" do
  password node["roundcube"]["db_pass"]
end
wosc_mysql_grant "roundcube" do
  user "roundcube"
end
execute "roundcube_db_schema" do
  command "mysql -Bs -uroot roundcube < /srv/roundcube/SQL/mysql.initial.sql"
  not_if "echo 'show tables' | mysql -uroot roundcube | grep -q ."
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/roundcube.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/mail.wosc.de" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/mail.wosc.de" do
  to "/etc/nginx/sites-available/mail.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end


package "imapproxy"
service "imapproxy"
execute "sed -i -e 's/#listen_address 127.0.0.1/listen_address 127.0.0.1/' /etc/imapproxy.conf" do
  only_if "grep -q '#listen_address' /etc/imapproxy.conf"
  notifies :restart, "service[imapproxy]", :delayed
end
