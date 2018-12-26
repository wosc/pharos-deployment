package "ruby"
package "ruby-mysql2"
gem_package "xmlrpc"

wosc_service_user "thyrida" do
  shell "/bin/bash"
end

cookbook_file "/srv/thyrida/app.tar.gz" do
  source "thyrida-2006-03-22+wosc.de+ruby2.3.tar.gz"
end
execute "tar xf /srv/thyrida/app.tar.gz -C /srv && chown -R thyrida: /srv/thyrida" do
  not_if "ls /srv/thyrida/Rakefile"
end

template "/srv/thyrida/config/database.yml" do
  source "database.yml"
  owner "thyrida"
  group "thyrida"
  mode "0640"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/thyrida.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/thyrida/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end


include_recipe "wosc-cgi"
directory "/srv/cgiserv/thyrida"
template "/srv/cgiserv/thyrida/start.sh" do
  source "start.sh"
  owner "cgiserv"
  group "cgiserv"
  mode "0774"
end

group "supervisor" do
  action :manage
  append true
  members "cgiserv"
end

file "/srv/cgiserv/apache.d/thyrida.conf" do
  content "ScriptAlias /start-thyrida /srv/cgiserv/thyrida/start.sh\n"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end


template "/srv/thyrida/maybe-stop.sh" do
  source "stop.sh"
  owner "thyrida"
  group "thyrida"
  mode "0755"
end

group "supervisor" do
  action :manage
  append true
  members "thyrida"
end

cron "stop thyrida when idle" do
  user "thyrida"
  minute "*/30"
  command "/srv/thyrida/maybe-stop.sh"
end
