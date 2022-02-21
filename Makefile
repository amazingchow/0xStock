.PHONY: code_check
code_check:
	@pyflakes data_tools/*.py
	@pyflakes store_tools/*.py
	@pycodestyle data_tools/*.py --ignore=E501,W504,E502,E131,E402,E302,W293
	@pycodestyle store_tools/*.py --ignore=E501,W504,E502,E131,E402,E302,W293

.PHONY: init_env
init_env:
	@./env_scripts/init_env.sh

.PHONY: clean_env
clean_env:
	@./env_scripts/clean_env.sh
