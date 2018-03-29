group "Debian-exim" do  # to run `mailq`
  action :manage
  append true
  members "prometheus"
end
template "/srv/prometheus/bin/node_exporter-mailq" do
  source "node_exporter-mailq.sh"
  mode "0755"
end
cron "mail-queue" do
  command "/srv/prometheus/bin/node_exporter-mailq"
  user "prometheus"
  mailto "wosc@wosc.de"
end

group "adm" do  # to read exim mainlog
  action :manage
  append true
  members "prometheus"
end
template "/srv/prometheus/bin/node_exporter-eximstats" do
  source "node_exporter-eximstats.sh"
  mode "0755"
end
cron "mail-stats" do
  command "/srv/prometheus/bin/node_exporter-eximstats"
  minute "*/5"
  user "prometheus"
  mailto "wosc@wosc.de"
end
