python_runtime "twifeed" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/usr/local/twifeed" do
  python "twifeed"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

template "/usr/local/twifeed/requirements.txt" do
  source "twifeed-requirements.txt"
end

pip_requirements "/usr/local/twifeed/requirements.txt" do
  virtualenv "/usr/local/twifeed"
  options "--no-deps"
end

# Install ws.twifeed manually from sdist, as it contains oauth secrets.

cron "twifeed-wosc" do
  command "/usr/local/twifeed/bin/twitter-notify"
  minute "0"
  user "wosc"
  mailto "wosc@wosc.de"
end
