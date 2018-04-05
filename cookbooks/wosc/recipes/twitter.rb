python_runtime "twifeed" do
  version "3.5"
  provider :system
end

python_virtualenv "/usr/local/twifeed" do
  python "twifeed"
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
