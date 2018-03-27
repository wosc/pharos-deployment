name             "wosc-wordpress"
version          "1.0.0"

maintainer       "Wolfgang Schnerring"
maintainer_email "wosc@wosc.de"
issues_url       nil
source_url       nil
license          "GPL"
description      ""
long_description IO.read(File.join(File.dirname(__FILE__), "README.md"))

chef_version     ">= 12"
supports         "ubuntu", ">= 16.04"

depends          "ark"
depends          "wosc"
depends          "wosc-fastcgi"
depends          "wosc-mysql"
