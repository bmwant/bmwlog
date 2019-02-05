.PHONY: tests

setup:
	@echo "Initial production provisioning..."
	@cd deploy/ansible && \
		ansible-playbook setup_centos.yml -i hosts -l digital_ocean -vv --ask-vault-pass

setup-freebsd:
	@echo "Initial production provisioning before deploy..."
	@cd deploy/ansible && \
		ansible-playbook setup_freebsd.yml -i hosts -l digital_ocean -vv --ask-vault-pass

update:
	@echo "Going to update bmwlog on production..."
	@cd deploy/ansible && \
		ansible-playbook update.yml -i hosts -l digital_ocean -vv --ask-vault-pass

tests:
	@py.test -sv -rs tests

flake:
	@flake . --count

clean:
	@echo "Removing cached files"
	@find . -name "*.pyc" -delete
