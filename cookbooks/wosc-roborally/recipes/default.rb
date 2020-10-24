VERSION = '1.0.0'

wosc_service_user "roborally" do
  shell "/bin/bash"
end

python_runtime "roborally" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/roborally/deployment" do
  user "roborally"
  group "roborally"
  python "roborally"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/roborally/requirements.txt" do
  source "requirements.txt"
  variables(version: VERSION)
end

pip_requirements "/srv/roborally/requirements.txt" do
  options "--no-deps"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/roborally.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart roborally" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/roborally/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
