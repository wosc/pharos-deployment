# Bootstrap a new server

```
# passwd   # (for root)
# dpkg-reconfigure locales
set default en_GB.utf8
# visudo
  Defaults timestamp_timeout=30
  Defaults:%sudo rootpw
# adduser wosc
# adduser wosc sudo
# hostname pharos
/etc/hosts: MYIP pharos.wosc.de pharos rz-hostname
/etc/hostname: pharos
# maybe set up local apt mirror

$ wosc ssh-copy-id
- restore /home/git/dot.git from Backup
$ git clone /home/git/dot .dot
$ .dot/shell/update-symlinks
$ ln -s ~/.dot/x11/github-notifier.cfg /home/wosc/gitmail
$ ln -s ~/.dot/x11/dailystrips.defs .dailystrips.defs
$ echo MYPASS > ~/.archivemail-wosc.de
- setup and run chef as described in Makefile
(cold run ca. 30 minutes, no-op ca. 2 minutes)
```

# Restore from backup

- /srv/letsencrypt/data/*/fullchain.pem
  wosc.de mail.wosc.de pharos.wosc.de grmusik.de
  mail.wosc.de/courier.pem
- mysql databases:
  mailserver
  grshop
  `# echo "UPDATE mailboxes SET uid=$(id -u Debian-exim), gid=$(id -g Debian-exim) | mysql mailserver"`
- /var/mail

- /srv/radicale/data
- /srvshaarli/public/data
- cd /srv/wallabag; php bin/console --env=prod wallabag:import --importer v2 --markAsRead true wosc wallabag-export.json (oder via mysql?)
- /var/spool/mlmmj
  /etc/mlmmj

- /home
  wosc controverse grmusik
- shadow password grmusik
- grshop/wp-content
