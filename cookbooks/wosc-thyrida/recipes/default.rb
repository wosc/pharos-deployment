package "ruby"
package "ruby-mysql"

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
  # XXX Too agressive since it restarts *all* services
  # notifies :reload, "service[supervisor]", :delayed
end


include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/thyrida.wosc.de" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/thyrida.wosc.de" do
  to "/etc/nginx/sites-available/thyrida.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end
