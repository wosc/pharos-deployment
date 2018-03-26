include_recipe "wosc-fastcgi::php"
package "php7.0-ctype"
package "php7.0-curl"
package "php7.0-mbstring"
package "php7.0-mcrypt"
package "php7.0-mysql"
package "php7.0-tokenizer"
package "php7.0-xml"
package "php7.0-xmlreader"
package "php7.0-xmlwriter"

wosc_service_user "agendav" do
  shell "/bin/bash"
end

VERSION = '2.2.0'

ark "agendav" do
  url "https://github.com/agendav/agendav/releases/download/#{VERSION}/agendav-#{VERSION}.tar.gz"
  action :put
  path "/srv"
  owner "agendav"
  group "agendav"
end

template "/srv/agendav/web/config/settings.php" do
  source "settings.php"
  owner "agendav"
  group "agendav"
  mode "0640"
end

wosc_mysql_database "agendav"
wosc_mysql_user "agendav" do
  password node["agendav"]["db_pass"]
end
wosc_mysql_grant "agendav" do
  user "agendav"
end

execute "agendav_db_schema" do
  command "php agendavcli migrations:migrate --no-interaction"
  cwd "/srv/agendav"
  not_if "echo 'show tables' | mysql -uroot agendav | grep -q ."
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/agendav.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/agendav/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
