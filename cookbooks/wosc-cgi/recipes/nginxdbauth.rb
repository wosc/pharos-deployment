package "libmysqlclient-dev"

python_runtime "nginxdbauth" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/srv/cgiserv/nginxdbauth" do
  user "cgiserv"
  group "cgiserv"
  python "nginxdbauth"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
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
