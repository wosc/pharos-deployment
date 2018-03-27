python_runtime "youtube" do
  version "3.5"
  provider :system
end

python_virtualenv "/usr/local/youtube" do
  python "youtube"
  setuptools_version "38.4.1"
  pip_version "9.0.1"
  wheel_version "0.30.0"
end

python_package "youtube-dl" do
  virtualenv "/usr/local/youtube"
end

link "/usr/local/bin/yt" do
  to "/usr/local/youtube/bin/youtube-dl"
end
