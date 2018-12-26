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


python_runtime "mailcheck" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end
python_virtualenv "/usr/local/mailcheck" do
  python "mailcheck"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/mailcheck/requirements.txt" do
  source "mailcheck-requirements.txt"
end
pip_requirements "/usr/local/mailcheck/requirements.txt" do
  virtualenv "/usr/local/mailcheck"
  options "--no-deps"
end

template "/srv/prometheus/mailcheck.conf" do
  source "mailcheck.conf"
  owner "prometheus"
  group "prometheus"
  mode "0600"
end
template "/srv/prometheus/caldavcheck.conf" do
  source "caldavcheck.conf"
  owner "prometheus"
  group "prometheus"
  mode "0600"
end

template "/srv/prometheus/bin/node_exporter-mailcheck" do
  source "node_exporter-mailcheck.sh"
  owner "prometheus"
  group "prometheus"
  mode "0755"
end
cron "mailcheck" do
  command "/srv/prometheus/bin/node_exporter-mailcheck"
  minute "*/5"
  user "prometheus"
  mailto "wosc@wosc.de"
end

template "/srv/prometheus/conf.d/alert-mailcheck.yml" do
  source "alert-mailcheck.yml"
  owner "prometheus"
  group "prometheus"
  notifies :run, "execute[reload prometheus]", :delayed
end
