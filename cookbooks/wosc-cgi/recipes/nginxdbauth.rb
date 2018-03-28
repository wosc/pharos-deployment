package "libmysqlclient-dev"

python_runtime "nginxdbauth" do
  version "3.5"
  provider :system
end

python_virtualenv "/srv/cgiserv/nginxdbauth" do
  user "cgiserv"
  group "cgiserv"
  python "nginxdbauth"
  setuptools_version "38.4.1"
  pip_version "9.0.1"
  wheel_version "0.30.0"
end

template "/srv/cgiserv/nginxdbauth/requirements.txt" do
  source "nginxdbauth/requirements.txt"
end

pip_requirements "/srv/cgiserv/nginxdbauth/requirements.txt" do
  virtualenv "/srv/cgiserv/nginxdbauth"
  options "--no-deps"
end

template "/srv/cgiserv/nginxdbauth/config" do
  source "nginxdbauth/auth.conf"
  owner "cgiserv"
  group "cgiserv"
  mode "0640"
end

template "/srv/cgiserv/apache.d/nginxdbauth.conf" do
  source "nginxdbauth/apache.conf"
  notifies :run, "execute[supervisorctl restart cgiserv]", :delayed
end
