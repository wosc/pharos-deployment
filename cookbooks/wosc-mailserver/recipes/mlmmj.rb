package "mlmmj"

package "bison"
ark "hypermail" do
  url "http://www.hypermail-project.org/hypermail-2.3.0.tar.gz"
  action :install_with_make
end

template "/usr/local/bin/mlmmj-update-archives" do
  source "mlmmj-update-archives.sh"
  mode "0755"
end

file "/etc/cron.d/mlmmj" do
  # The first line is from the deb package
  content "0 */2 * * * root /usr/bin/test -x /usr/bin/mlmmj-maintd && /usr/bin/mlmmj-maintd -F -d /var/spool/mlmmj\n5 */2 * * * root /usr/local/bin/mlmmj-update-archives"
end
