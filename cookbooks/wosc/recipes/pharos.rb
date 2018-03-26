include_recipe "wosc-fastcgi::nginx"
template "/etc/nginx/sites-available/pharos.wosc.de" do
  source "pharos.wosc.de.conf"
  notifies :reload, "service[nginx]", :delayed
end
link "/etc/nginx/sites-enabled/pharos.wosc.de" do
  to "/etc/nginx/sites-available/pharos.wosc.de"
  notifies :reload, "service[nginx]", :delayed
end

template "/etc/motd" do
  source "motd.txt"
end
