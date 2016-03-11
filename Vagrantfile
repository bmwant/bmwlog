VAGRANTFILE_API_VERSION = "2"
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "freebsd"
  config.vm.network "private_network", ip: "10.0.7.7"
  #config.vm.synced_folder ".", "/home/vagrant/workspace/shrink"
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "vv"
    ansible.playbook = "local/ansible/setup.yml"
  end
  config.ssh.forward_agent = true
end
