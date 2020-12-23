# Bootstrap a new server

```
# passwd   # (for root)
# dpkg-reconfigure locales
set default en_GB.utf8
# adduser wosc
# adduser wosc sudo
# hostname pharos
/etc/hosts: MYIP pharos.wosc.de pharos rz-hostname
/etc/hostname: pharos
# maybe set up local apt mirror
# dd if=/dev/zero of=/swapfile bs=1024 count=$((2048*1024))
# chmod 600 /swapfile
# mkswap /swapfile
# swapon /swapfile
# echo "/swapfile none swap sw 0 0" >> /etc/fstab

$ wosc ssh-copy-id
- restore /home/git/dot.git from Backup
$ git clone /home/git/dot .dot
$ .dot/shell/update-symlinks
$ ln -s ~/.dot/x11/github-notifier.cfg /home/wosc/gitmail
$ ln -s ~/.dot/x11/dailystrips.defs .dailystrips.defs

# apt install python3-venv
# sudo echo 'wosc ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/batou
$ ./batou deploy production
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
