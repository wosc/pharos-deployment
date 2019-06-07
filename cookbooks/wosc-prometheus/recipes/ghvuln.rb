python_runtime "ghvuln" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end
python_virtualenv "/usr/local/ghvuln" do
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/ghvuln/requirements.txt" do
  source "ghvuln-requirements.txt"
end
pip_requirements "/usr/local/ghvuln/requirements.txt" do
  virtualenv "/usr/local/ghvuln"
  options "--no-deps"
end

template "/etc/supervisor/conf.d/prometheus-ghvuln.conf" do
  source "supervisor/ghvuln_exporter.conf"
  notifies :run, "execute[reload_supervisor]", :delayed
end

template "/srv/prometheus/conf.d/alert-ghvuln.yml" do
  source "alert-ghvuln.yml"
  owner "prometheus"
  group "prometheus"
  notifies :run, "execute[reload prometheus]", :delayed
end
