install:
	@local/scripts/install.sh

update:
    cd local/ansible
    @ansible-playbook update.yml
