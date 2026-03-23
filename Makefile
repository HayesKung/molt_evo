install:
	bash install.sh

upgrade:
	bash upgrade.sh

uninstall:
	bash uninstall.sh

healthcheck:
	bash healthcheck.sh

selftest:
	bash selftest.sh

bootstrap:
	bash bootstrap.sh

release:
	bash manage.sh release

export:
	python3 jarvis_export.py
