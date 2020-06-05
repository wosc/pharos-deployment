wosc_service_user "prometheus" do
  shell "/bin/bash"
end

[
  "bin",
  "conf.d",
  "data",
  "node",
].each do |dir|
    directory "/srv/prometheus/#{dir}" do
      owner "prometheus"
      group "prometheus"
    end
end

VERSION = '2.18.1'
NODE_VERSION = '1.0.0'

ark "prometheus" do
  url "https://github.com/prometheus/prometheus/releases/download/v#{VERSION}/prometheus-#{VERSION}.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/prometheus' '*/promtool'"
  path "/srv/prometheus/bin"
end
ark "node_exporter" do
  url "https://github.com/prometheus/node_exporter/releases/download/v#{NODE_VERSION}/node_exporter-#{NODE_VERSION}.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*node_exporter'"
  path "/srv/prometheus/bin"
end
ark "pushgateway" do
  url "https://github.com/prometheus/pushgateway/releases/download/v0.4.0/pushgateway-0.4.0.linux-amd64.tar.gz"
  action :cherry_pick
  creates "--wildcards '*/pushgateway'"
  path "/srv/prometheus/bin"
end

template "/srv/prometheus/server.yml" do
  source "server.yml"
  owner "prometheus"
  group "prometheus"
  notifies :run, "execute[reload prometheus]", :delayed
end

include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/prometheus.conf" do
  source "supervisor/prometheus.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end
template "/etc/supervisor/conf.d/prometheus-node.conf" do
  source "supervisor/node_exporter.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end
# template "/etc/supervisor/conf.d/prometheus-push.conf" do
#   source "supervisor/pushgateway.conf"
#   notifies :run, "execute[reload_supervisor]", :delayed
# end

execute "reload prometheus" do
  command "kill -HUP $(supervisorctl pid prometheus)"
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/prometheus/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end

# node_exporter doesn't expose total number of processes, unsure whether
# <https://github.com/prometheus/node_exporter/issues/790> will help.
template "/srv/prometheus/bin/node_exporter-numprocs" do
  source "node_exporter-numprocs.sh"
  mode "0755"
end
cron "numprocs" do
  command "/srv/prometheus/bin/node_exporter-numprocs"
  user "prometheus"
  mailto "wosc@wosc.de"
end
