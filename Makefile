.PHONY: code_check
code_check:
	@pyflakes datatool/*.py
	@pyflakes storetool/*.py
	@pycodestyle datatool/*.py --ignore=E501,W504,E502,E131,E402,E302,W293
	@pycodestyle storetool/*.py --ignore=E501,W504,E502,E131,E402,E302,W293

.PHONY: init_env
init_env:
	@./scripts/init_env.sh

.PHONY: clean_env
clean_env:
	@./scripts/clean_env.sh
