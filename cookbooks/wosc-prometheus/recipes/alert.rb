directory "/srv/prometheus/data/alerts" do
  owner "prometheus"
  group "prometheus"
end

VERSION = '0.17.0'

ark "alertmanager" do
  url "https://github.com/prometheus/alertmanager/releases/download/v#{VERSION}/alertmanager-#{VERSION}.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/alertmanager' '*/amtool'"
  path "/srv/prometheus/bin"
end

template "/srv/prometheus/alert.yml" do
  source "alert.yml"
  owner "prometheus"
  group "prometheus"
  notifies :run, "execute[reload alertmanager]", :delayed
end
execute "reload alertmanager" do
  command "kill -HUP $(supervisorctl pid prometheus-alert)"
  action :nothing
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/prometheus-alert.conf" do
  source "supervisor/alert.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end


template "/srv/prometheus/bin/send-alert" do
  source "send-alert.sh"
  mode "0755"
end
