wosc_service_user "letsencrypt" do
  shell "/bin/bash"
end

group "letsencrypt" do
  action :manage
  append true
  members "www-data"
  only_if "id -a www-data"
end

group "letsencrypt" do
  action :manage
  append true
  members "Debian-exim"
  only_if "id -a Debian-exim"
end

include_recipe "wosc-letsencrypt::items"


# Install simp_le client <https://github.com/zenhack/simp_le>

python_runtime "letsencrypt" do
  version "3.6"
  provider :system
end

python_virtualenv "/srv/letsencrypt/deployment" do
  user "letsencrypt"
  group "letsencrypt"
  python "letsencrypt"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/srv/letsencrypt/requirements.txt" do
  source "requirements.txt"
end

pip_requirements "/srv/letsencrypt/requirements.txt" do
  virtualenv "/srv/letsencrypt/deployment"
  options "--no-deps"
end

template "/usr/local/src/simple-logging.patch" do
  source "simple-logging.patch"
end
execute "patch -p0 < /usr/local/src/simple-logging.patch" do
  not_if "grep -q 'wosc patched' /srv/letsencrypt/deployment/lib/python3.6/site-packages/simp_le.py"
end


# nginx integration

template "/etc/nginx/snippets/letsencrypt.conf" do
  source "nginx.conf"
end

template "/etc/sudoers.d/letsencrypt" do
  source "sudo.conf"
end
template "/srv/letsencrypt/update-letsencrypt" do
  source "update-letsencrypt"
  mode "0755"
  owner "letsencrypt"
  group "letsencrypt"
end

cron "update-letsencrypt" do
  command "/srv/letsencrypt/update-letsencrypt"
  hour "2"
  minute "15"
  user "letsencrypt"
  mailto "wosc@wosc.de"
end
