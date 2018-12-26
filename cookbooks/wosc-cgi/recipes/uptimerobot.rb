python_runtime "uptimerobot" do
  version "3.6"
  provider :system
end

python_virtualenv "/srv/cgiserv/uptimerobot" do
  user "cgiserv"
  group "cgiserv"
  python "uptimerobot"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/cgiserv/uptimerobot/requirements.txt" do
  source "uptimerobot/requirements.txt"
end

pip_requirements "/srv/cgiserv/uptimerobot/requirements.txt" do
  virtualenv "/srv/cgiserv/uptimerobot"
  options "--no-deps"
end

template "/srv/cgiserv/uptimerobot/config" do
  source "uptimerobot/uptimerobot.conf"
  owner "cgiserv"
  group "cgiserv"
  mode "0640"
end

template "/srv/cgiserv/apache.d/uptimerobot.conf" do
  source "uptimerobot/apache.conf"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end
