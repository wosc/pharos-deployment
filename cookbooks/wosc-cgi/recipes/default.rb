package "apache2"
service "apache2" do
  action :disable
end

wosc_service_user "cgiserv" do
  shell "/bin/bash"
end

directory "/srv/cgiserv/apache.d"
directory "/srv/cgiserv/nginx.d"

template "/srv/cgiserv/apache.conf" do
  source "apache.conf"
  owner "cgiserv"
  group "cgiserv"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/cgiserv.conf" do
  source "supervisor.conf"
  # XXX Too agressive since it restarts *all* services
  # notifies :reload, "service[supervisor]", :delayed
end

execute "supervisorctl restart cgiserv" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/cgi.wosc.de" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/cgi.wosc.de" do
  to "/etc/nginx/sites-available/cgi.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end
