PRODUCTION_HOST = pharos.wosc.de

# Bootstrap:
# * apt-get install build-essential
# * Install chef-client-13.x from <https://downloads.chef.io/chef>
# * Set up paswordless sudo for /usr/bin/chef-client
production:
	@rsync -a Makefile client.rb $(CURDIR)/cookbooks $(CURDIR)/nodes $(PRODUCTION_HOST):chef
	@ssh $(PRODUCTION_HOST) make -C ./chef deploy

deploy:
	sudo chef-client --local-mode --config $(CURDIR)/client.rb -j $(CURDIR)/nodes/$(PRODUCTION_HOST).json


.PHONY: production deploy
