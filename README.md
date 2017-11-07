# Build system to get Jenkins/Gitlab/Artifactory environment in AWS

All of the components are installed on a VM, using standard(ish) docker images with 
some minor alterations.

Initial creation based on Vagrant, with a plan to move to packer to create an AMI
