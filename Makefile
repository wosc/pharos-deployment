PRODUCTION_HOST = pharos.wosc.de

# Bootstrap:
# * apt-get install build-essential
# * Install chef-client-13.x from <https://downloads.chef.io/chef>
# * sudo echo 'wosc ALL=(root) NOPASSWD: /usr/bin/chef-client' > /etc/sudoers.d/chef
.PHONY: production
production: build/.berks.success
	@rsync -a Makefile client.rb $(CURDIR)/cookbooks $(CURDIR)/nodes $(PRODUCTION_HOST):chef
	@rsync -a --exclude "wosc*" build/ $(PRODUCTION_HOST):chef/cookbooks/
	@ssh $(PRODUCTION_HOST) make -C ./chef deploy

.PHONY: deploy
deploy:
	sudo chef-client --local-mode --config $(CURDIR)/client.rb -j $(CURDIR)/nodes/$(PRODUCTION_HOST).json


.PHONY: berks
berks: build/.berks.success
build/.berks.success: Berksfile Berksfile.lock
	berks vendor $(CURDIR)/build
	@touch $@
