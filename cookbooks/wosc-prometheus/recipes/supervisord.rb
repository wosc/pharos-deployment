group "supervisor" do  # to access supervisor control socket
  action :manage
  append true
  members "prometheus"
end
template "/srv/prometheus/bin/node_exporter-supervisord" do
  source "node_exporter-supervisord.py"
  mode "0755"
end
cron "supervisord" do
  command "/srv/prometheus/bin/node_exporter-supervisord"
  user "prometheus"
  mailto "wosc@wosc.de"
end
