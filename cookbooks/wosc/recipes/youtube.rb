python_runtime "youtube" do
  version "3.6"
  provider :system
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
end

python_virtualenv "/usr/local/youtube" do
  python "youtube"
  get_pip_url "https://github.com/pypa/get-pip/raw/f88ab195ecdf2f0001ed21443e247fb32265cabb/get-pip.py"
  pip_version node["python"]["pip_version"]
  setuptools_version node["python"]["setuptools_version"]
  wheel_version node["python"]["wheel_version"]
end

python_package "youtube-dl" do
  virtualenv "/usr/local/youtube"
end

link "/usr/local/bin/yt" do
  to "/usr/local/youtube/bin/youtube-dl"
end
