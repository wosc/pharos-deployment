# Unlock encrypted repository

```
apt install git git-crypt
git clone git@github.com:wosc/pharos-deployment.git pharos
cd pharos
git crypt unlock
```

# Bootstrap a new server

```
# passwd   # (for root)
# sed -i -e "s/^mesg n.*$/tty -s \&\& mesg n/" /root/.profile
# dpkg-reconfigure locales
set default en_GB.utf8
# adduser wosc
# adduser wosc sudo
# echo "pharos.wosc.de" > /etc/hostname
# maybe set up local apt mirror
# dd if=/dev/zero of=/swapfile bs=1024 count=$((2048*1024))
# chmod 600 /swapfile
# mkswap /swapfile
# swapon /swapfile
# echo "/swapfile none swap sw 0 0" >> /etc/fstab
# echo "network: {config: disabled}" > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
# cat > /etc/netplan/01-static.yaml <<EOF
network:
  version: 2
  ethernets:
    eth0:
      addresses:
      - MYIPV4/32
      - MYIPV6/64
      # https://docs.hetzner.com/cloud/servers/static-configuration
      routes:
      - to: 0.0.0.0/0
        via: 172.31.1.1
        on-link: true
      - to: default
        via: fe80::1
      nameservers:
        addresses:
        - 185.12.64.1
        - 185.12.64.2
        - 2a01:4ff:ff00::add:1
        - 2a01:4ff:ff00::add:2
EOF

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
