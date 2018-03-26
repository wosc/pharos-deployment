VERSION = "2.48.3-1ubuntu1"

package "unison" do
  # Must match the version on the client laptop(s)!
  version VERSION
end

file "/etc/apt/preferences.d/unison" do
  content "Package: unison\nPin: version #{VERSION}\nPin-Priority: 999\n"
end

directory "/home/wosc/.ssh" do
  owner "wosc"
  group "wosc"
end
template "/home/wosc/.ssh/authorized_keys" do
  source "authorized_keys"
  owner "wosc"
  group "wosc"
  mode "06400"
end
template "/usr/local/bin/ssh-accept-unison" do
  source "ssh-accept-unison"
  mode "0755"
end


[
  "/home/wosc/sync",
  "/home/wosc/tmp",
].each do |dir|
  directory dir do
    owner "wosc"
    group "wosc"
  end
end
