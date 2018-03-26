include_recipe "wosc-fastcgi::php"
package "php7.0-bcmath"
package "php7.0-curl"
package "php7.0-gd"
package "php7.0-gettext"
package "php7.0-mbstring"
package "php7.0-mysql"
package "php7.0-tidy"
package "php7.0-xml"

wosc_service_user "wallabag" do
  shell "/bin/bash"
end

VERSION = '2.3.2'

ark "wallabag" do
  url "http://static.wallabag.org/releases/wallabag-release-#{VERSION}.tar.gz"
  action :put
  path "/srv"
  owner "wallabag"
  group "wallabag"
end

template "/srv/wallabag/app/config/parameters.yml" do
  source "parameters.yml"
  owner "wallabag"
  group "wallabag"
  mode "0640"
end

wosc_mysql_database "wallabag"
wosc_mysql_user "wallabag" do
  password node["wallabag"]["db_pass"]
end
wosc_mysql_grant "wallabag" do
  user "wallabag"
end

execute "wallabag_db_schema" do
  command "php bin/console --env=prod wallabag:install --no-interaction; chown -R wallabag: /srv/wallabag/var"
  cwd "/srv/wallabag"
  not_if "echo 'show tables' | mysql -uroot wallabag | grep -q ."
end

execute "wallabag_admin_password" do
  command "php bin/console --env=prod fos:user:change-password wallabag #{node['wallabag']['root_pass']}"
  cwd "/srv/wallabag"
  not_if "echo 'select username from wallabag_user' | mysql wallabag | grep -q root"
end
execute "wallabag_admin_login" do
  command "echo 'update wallabag_user set username=\"root\", username_canonical=\"root\"' | mysql wallabag"
  not_if "echo 'select username from wallabag_user' | mysql wallabag | grep -q root"
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/wallabag.conf" do
  source "supervisor.conf"
  # XXX Too agressive since it restarts *all* services
  # notifies :reload, "service[supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/reader.wosc.de" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/reader.wosc.de" do
  to "/etc/nginx/sites-available/reader.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end
