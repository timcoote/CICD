# -*- mode: ruby -*-
# vi: set ft=ruby :

# Merge virtualbox and aws vm SD card builder.
#
# need to add this box:
# vagrant box add dummy https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box
#Vagrant.require_plugin "vagrant-aws"

Vagrant.configure("2") do |config|
   config.ssh.forward_agent=true

 
   config.vm.provider "aws" do |aws, override|
      config.vm.box = "dummy"
      aws.region = "eu-west-1"
      aws.ami = "ami-add175d4"
      aws.security_groups = ['launch-wizard-4']
#      override.ssh.private_key_path = "~/.ssh/iotaa.pem"
      override.ssh.private_key_path = "~/.ssh/iotaa.pem"
      override.ssh.username = "ubuntu"
      aws.keypair_name = "iotaa"
      aws.instance_type = "m4.large"
      aws.block_device_mapping = [{ 'DeviceName' => '/dev/sda1', 'Ebs.VolumeSize' => 50 }]
# avoid rsyncing any local build
#      override.vm.synced_folder ".", "/vagrant", disabled: true
      aws.tags = {
          'Name' => 'CICD'
      }
   end

   config.vm.provision "file", source: "~/.aws/credentials", destination: "/home/ubuntu/.aws/credentials"

   config.vm.provision "shell", inline: <<-SHELL
      sudo apt install -y python-minimal
# kept for ease of extension
   SHELL

   config.vm.provision "ansible" do |ansible|
     ansible.playbook = "site.yml"
     ansible.force_remote_user = true 
   end

end
