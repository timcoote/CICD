# -*- mode: ruby -*-
# vi: set ft=ruby :

# Merge virtualbox and aws vm SD card builder.
#
# need to add this box:
# vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box
#Vagrant.require_plugin "vagrant-aws"

Vagrant.configure("2") do |config|
   config.vm.network "public_network", bridge: "en0: Wi-Fi (AirPort)"  # use external dhcp so that other rfc 1918 machines can be reached
#   config.vm.provision "file", source: "./loops", destination: "/home/fedora/loops"
   config.ssh.forward_agent=true

   user = "fedora"
   config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
     config.vm.box = "bento/fedora-26" # capsh fails to drop capability, although error message is that it cannot be raised ?
     vb.customize ["modifyvm", :id, "--memory", "2048"]
     vb.customize ["modifyvm", :id, "--cpus", "2"]
   end
 
   if user != "vagrant"
     config.vm.provider "aws" do |aws, override|
      config.vm.box = "dummy"
      aws.region = "eu-west-1"
      aws.ami = "ami-aac928d3"
      aws.security_groups = ['launch-wizard-4']
      override.ssh.username = "fedora"
      override.ssh.private_key_path = "~/.ssh/dublinkeypair.pem"
      aws.keypair_name = "dublinkeypair"
      aws.instance_type = "m4.large"
      aws.block_device_mapping = [{ 'DeviceName' => '/dev/sda1', 'Ebs.VolumeSize' => 50 }]
# avoid rsyncing any local build
      override.vm.synced_folder ".", "/vagrant", disabled: true
     end
   end

   config.vm.provision "file", source: "~/.aws/credentials", destination: "/home/#{user}/.aws/credentials"

   config.vm.provision "shell", inline: <<-SHELL
      dnf install -y docker-compose docker python3-dateutil rng-tools rake awscli python git libselinux-python
      su "#{user}" -c "mkdir -p /home/#{user}/.ssh"
      su "#{user}" -c "ssh-keyscan -H github.com >> /home/#{user}/.ssh/known_hosts"
      su "#{user}" -c "chmod 600 ~/.ssh/known_hosts"
      su "#{user}" -c "ssh -T git@github.com"
      su "#{user}" -c "git clone ssh://git@github.com/timcoote/Pumpkin-gen.git"
# moved to ansible      su "#{user}" -c "touch /home/#{user}/Pumpkin-gen/{export-noobs,stage5}/SKIP"
# need this to generate enough entropy for gpg --gen-key
      rngd -r /dev/urandom
      systemctl enable docker
      systemctl start docker
      sh -x /home/#{user}/Pumpkin-gen/loops
# now in ansible      chown root:fedora /var/run/docker.sock   # throws error, cannot find the file?
      echo -n ":arm:M::\\x7fELF\\x01\\x01\\x01\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x02\\x00\\x28\\x00:\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\x00\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xff\\xfe\\xff\\xff\\xff:/usr/bin/qemu-arm-static:" > /proc/sys/fs/binfmt_misc/register  || true # true in case the scrips has run before
      su "#{user}" -c "cd Pumpkin-gen && rake"
    SHELL

   config.vm.provision "ansible" do |ansible|
     ansible.playbook = "site.yml"
     ansible.force_remote_user = true 
   end

end
