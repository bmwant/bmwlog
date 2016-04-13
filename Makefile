.PHONY: tests

install:
	@local/scripts/install.sh

update:
	@echo "Going to update bmwlog on production..."
	@cd local/ansible && \
	ansible-playbook update.yml -i hosts -l mfhoster -vv --ask-sudo-pass

tests:
	@py.test -sv -rs tests


style-check:
	@pep8 . --first --count
