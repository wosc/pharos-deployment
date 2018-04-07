[
  "archivemail",
  "bsd-mailx",
  "fetchmail",
  "mutt",
  "t-prot",
  "urlview",
].each do |name|
  package name
end

template "/usr/local/src/archivemail-username.patch" do
  source "archivemail-username.patch"
end
execute "patch -p0 < /usr/local/src/archivemail-username.patch" do
  not_if "grep -q 'wosc patched' /usr/bin/archivemail"
end


cron "archivemail-copy" do
  command "archivemail --days=14 --delete --output-dir=/tmp --pwfile /home/wosc/.archivemail-wosc.de 'imaps://wosc@wosc.de#mail.wosc.de/INBOX.copy' > /dev/null"
  minute "10"
  hour "0"
  user "wosc"
  mailto "wosc@wosc.de"
end
cron "archivemail-spam" do
  command "archivemail --days=7 --delete --output-dir=/tmp --pwfile /home/wosc/.archivemail-wosc.de 'imaps://wosc@wosc.de#mail.wosc.de/INBOX.Spam' > /dev/null"
  minute "10"
  hour "0"
  user "wosc"
  mailto "wosc@wosc.de"
end

cron "notify reboot" do
  command "sleep 30; echo `date` | /usr/bin/mail -s 'pharos rebooted' wosc@localhost"
  time :reboot
  user "wosc"
  mailto "wosc@wosc.de"
end

cron "fetchmail" do
  command "/usr/bin/fetchmail -f /home/wosc/.dot/mail/fetchmailrc-pharos"
  time :reboot
  user "wosc"
  mailto "wosc@wosc.de"
end
