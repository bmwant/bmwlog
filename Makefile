.PHONY: tests

install:
	@local/scripts/install.sh

setup-freebsd:
	@echo "Initial production provisioning before deploy"
	@cd local/ansible && \
		ansible-playbook setup_freebsd.yml -i hosts -l digital_ocean -vv --ask-vault-pass

update:
	@echo "Going to update bmwlog on production..."
	@cd local/ansible && \
		ansible-playbook update.yml -i hosts -l digital_ocean -vv --ask-vault-pass

tests:
	@py.test -sv -rs tests

style-check:
	@pep8 . --count

clean:
	@echo "Removing cached files"
	@find . -name "*.pyc" -delete
