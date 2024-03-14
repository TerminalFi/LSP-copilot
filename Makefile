$(VERBOSE).SILENT:

.PHONY: all
all:

.PHONY: check
check:
	( \
		$(MAKE) -f Makefile.check pre-check; \
		$(MAKE) -f Makefile.check check; \
		EXIT_CODE=$$?; \
		$(MAKE) -f Makefile.check post-check; \
		exit $$EXIT_CODE \
	)

.PHONY: fix
fix:
	autoflake --in-place .
	black .
	isort .
