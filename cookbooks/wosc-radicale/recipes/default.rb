VERSION = '1.1.6'
# XXX Version 2.x removes the "ics-file" storage backend

wosc_service_user "radicale" do
  shell "/bin/bash"
end

directory "/srv/radicale/data" do
  owner "radicale"
  group "radicale"
end

python_runtime "radicale" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/radicale/deployment" do
  user "radicale"
  group "radicale"
  python "radicale"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/radicale/requirements.txt" do
  source "requirements.txt"
  variables(version: VERSION)
end

pip_requirements "/srv/radicale/requirements.txt" do
  options "--no-deps"
end

execute "sed -i -e 's/sock.send(line)/sock.send(line.encode(\"utf-8\"))/' -e 's/\"GID\"/b\"GID\"/' -e 's/except Exception:/except Exception as exception/' /srv/radicale/deployment/lib/python3.6/site-packages/radicale/auth/courier.py" do
  not_if "grep -q 'b\"GID\"' /srv/radicale/deployment/lib/python3.6/site-packages/radicale/auth/courier.py"
end

template "/srv/radicale/radicale.conf" do
  source "radicale.conf"
  owner "radicale"
  group "radicale"
  notifies :run, "execute[supervisorctl restart radicale]", :delayed
end

template "/srv/radicale/logging.conf" do
  source "logging.conf"
  owner "radicale"
  group "radicale"
  notifies :run, "execute[supervisorctl restart radicale]", :delayed
end

template "/srv/radicale/serve.py" do
  source "serve.py"
  owner "radicale"
  group "radicale"
  notifies :run, "execute[supervisorctl restart radicale]", :delayed
end

group "courier" do
  action :manage
  append true
  members "radicale"
end


include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/radicale.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart radicale" do
  action :nothing
end

# Socket is created by serve.py as user radicale, so we need to allow nginx
# to read from it.
group "radicale" do
  action :manage
  append true
  members "www-data"
  only_if "id -a www-data"
end

include_recipe "wosc-fastcgi::nginx"
template "/srv/radicale/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end
