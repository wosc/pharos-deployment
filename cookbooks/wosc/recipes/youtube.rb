python_runtime "youtube" do
  version "3.6"
  provider :system
end

python_virtualenv "/usr/local/youtube" do
  python "youtube"
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
