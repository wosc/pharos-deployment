python_runtime "rsspull" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/usr/local/rsspull" do
  python "rsspull"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/rsspull/requirements.txt" do
  source "rsspull-requirements.txt"
end

pip_requirements "/usr/local/rsspull/requirements.txt" do
  virtualenv "/usr/local/rsspull"
  options "--no-deps"
end

link "/usr/local/bin/rsspull" do
  to "/usr/local/rsspull/bin/rsspull"
end

cron "rsspull-wosc" do
  command "/usr/local/rsspull/bin/rsspull --confdir=/home/wosc/.dot/x11/rsspull"
  hour "6"
  minute "0"
  user "wosc"
  mailto "wosc@wosc.de"
end
cron "rsspull-kolumbus" do
  command "/usr/local/rsspull/bin/rsspull --confdir=/home/wosc/.dot/x11/rsspull-kolumbus"
  hour "6"
  minute "0"
  user "wosc"
  mailto "wosc@wosc.de"
end

group "Debian-exim" do  # so we can write to Maildir directly
  action :manage
  append true
  members "wosc"
end
