install:
	bash manage.sh install

upgrade:
	bash manage.sh upgrade

uninstall:
	bash manage.sh uninstall

healthcheck:
	bash manage.sh healthcheck

selftest:
	bash manage.sh selftest

bootstrap:
	bash manage.sh bootstrap

release:
	bash manage.sh release

export:
	bash manage.sh export

import:
	@echo "Usage: bash manage.sh import /path/to/export.json merge"
