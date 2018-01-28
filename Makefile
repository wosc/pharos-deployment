PRODUCTION_HOST = pharos.wosc.de

# Bootstrap:
# * apt-get install build-essential
# * Install chef-client-13.x from <https://downloads.chef.io/chef>
# * Set up paswordless sudo for /usr/bin/chef-client
production: build/.berks.success
	@rsync -a Makefile client.rb $(CURDIR)/cookbooks $(CURDIR)/nodes $(PRODUCTION_HOST):chef
	@rsync -a --exclude "wosc*" build/ $(PRODUCTION_HOST):chef/cookbooks/
	@ssh $(PRODUCTION_HOST) make -C ./chef deploy

deploy:
	sudo chef-client --local-mode --config $(CURDIR)/client.rb -j $(CURDIR)/nodes/$(PRODUCTION_HOST).json


build/.berks.success: Berksfile
	berks vendor $(CURDIR)/build
	@touch $@


.PHONY: production deploy
