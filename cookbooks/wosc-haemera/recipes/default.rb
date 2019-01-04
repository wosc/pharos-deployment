VERSION = '1.0.0'

wosc_service_user "haemera" do
  shell "/bin/bash"
end

python_runtime "haemera" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/haemera/deployment" do
  user "haemera"
  group "haemera"
  python "haemera"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/haemera/requirements.txt" do
  source "requirements.txt"
  variables(version: VERSION)
end

pip_requirements "/srv/haemera/requirements.txt" do
  options "--no-deps"
end

template "/srv/haemera/paste.ini" do
  source "paste.ini"
  owner "haemera"
  group "haemera"
  notifies :run, "execute[supervisorctl restart haemera]", :delayed
end

wosc_mysql_database "haemera"
wosc_mysql_user "haemera" do
  password node["haemera"]["db_pass"]
end
wosc_mysql_grant "haemera" do
  user "haemera"
end
execute "haemera_db_schema" do
  command "/srv/haemera/deployment/bin/haemera-init-db /srv/haemera/paste.ini#haemera"
  not_if "echo 'show tables' | mysql -uroot haemera | grep -q ."
end



include_recipe "wosc-fastcgi::supervisor"
template "/etc/supervisor/conf.d/haemera.conf" do
  source "supervisor.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

execute "supervisorctl restart haemera" do
  action :nothing
end


include_recipe "wosc-fastcgi::nginx"
template "/srv/haemera/nginx.conf" do
  source "nginx.conf"
  notifies :reload, "service[nginx]", :delayed
end


cron "haemera-recurrence" do
  command "/srv/haemera/deployment/bin/haemera-recurrences /srv/haemera/paste.ini#haemera"
  hour "0"
  minute "5"
  user "haemera"
  mailto "wosc@wosc.de"
end
