VERSION = '2.0.0'

wosc_service_user "thyrida" do
  shell "/bin/bash"
end

python_runtime "thyrida" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/thyrida/deployment" do
  user "thyrida"
  group "thyrida"
  python "thyrida"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/thyrida/requirements.txt" do
  source "requirements.txt"
  variables(version: VERSION)
end

pip_requirements "/srv/thyrida/requirements.txt" do
  options "--no-deps"
end

template "/srv/thyrida/paste.ini" do
  source "paste.ini"
  owner "thyrida"
  group "thyrida"
  notifies :run, "execute[supervisorctl restart thyrida]", :delayed
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/thyrida.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart thyrida" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/thyrida/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
