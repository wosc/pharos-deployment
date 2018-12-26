include_recipe "wosc-fastcgi::php"
package "php7.2-bcmath"
package "php7.2-curl"
package "php7.2-gd"
package "php7.2-gettext"
package "php7.2-mbstring"
package "php7.2-mysql"
package "php7.2-tidy"
package "php7.2-xml"

wosc_service_user "wallabag" do
  shell "/bin/bash"
end

VERSION = '2.3.3'

ark "wallabag" do
  url "http://static.wallabag.org/releases/wallabag-release-#{VERSION}.tar.gz"
  action :put
  path "/srv"
  owner "wallabag"
  group "wallabag"
end

template "/usr/local/src/wallabag-backup-api.patch" do
  source "backup-api.patch"
end
execute "patch -p0 < /usr/local/src/wallabag-backup-api.patch" do
  not_if "grep -q backup /srv/wallabag/app/config/routing.yml"
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
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/wallabag/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
