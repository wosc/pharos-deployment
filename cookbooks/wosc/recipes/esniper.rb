[
  "libssl-dev",
  "libcurl4-gnutls-dev"
].each do |name|
  package name
end

VERSION = "848382f44579b3441dece67cbfe415e4ab64ff5d"

directory "/usr/local/esniper-1"

# We abuse this `ark` step to patch the source
file "/usr/local/esniper-1/autogen.sh" do
  content "sed -i -e 's/#define MIN_BIDTIME 5/#define MIN_BIDTIME 2/' /usr/local/esniper-1/esniper.c"
  mode "0755"
end

# XXX The zip URL only exists after you've clicked on "download snapshot" at
# https://sourceforge.net/p/esniper/git/ci/848382f44579b3441dece67cbfe415e4ab64ff5d/tree/
ark "esniper" do
  url "https://sourceforge.net/code-snapshots/git/e/es/esniper/git.git/esniper-git-#{VERSION}.zip"
  action :install_with_make
  not_if "ls /usr/local/bin/esniper"
end
