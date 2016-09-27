.PHONY: tests

install:
	@local/scripts/install.sh

setup:
	@echo "Initial production provisioning before deploy"
	@cd local/ansible && \
		ansible-playbook setup.yml -i hosts -l digital_ocean -vv --ask-sudo-pass

update:
	@echo "Going to update bmwlog on production..."
	@cd local/ansible && \
		ansible-playbook update.yml -i hosts -l digital_ocean -vv --ask-sudo-pass

tests:
	@py.test -sv -rs tests

style-check:
	@pep8 . --count
