VERSION = '1.0.0'

wosc_service_user "tabu" do
  shell "/bin/bash"
end

python_runtime "tabu" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/tabu/deployment" do
  user "tabu"
  group "tabu"
  python "tabu"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/tabu/requirements.txt" do
  source "requirements.txt"
  variables(version: VERSION)
end

pip_requirements "/srv/tabu/requirements.txt" do
  options "--no-deps"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/tabu.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart tabu" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/tabu/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
