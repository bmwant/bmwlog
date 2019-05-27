.PHONY: tests

setup:
	@echo "Initial production provisioning..."
	@cd deploy/ansible && \
		ansible-playbook setup_centos.yml -i hosts -l digital_ocean -vv --ask-vault-pass

update:
	@echo "Going to update bmwlog on production..."
	@cd deploy/ansible && \
		poetry run \
		ansible-playbook update.yml -i hosts -l digital_ocean -vv --ask-vault-pass

tests:
	@pytest -sv -rs tests

flake:
	@flake8 . --count

clean:
	@echo "Removing cached files"
	@find . -name "*.pyc" -delete
