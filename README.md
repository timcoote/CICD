# Build system to get Jenkins/Gitlab/Artifactory environment in AWS

* All of the components are installed on a VM, using standard(ish) docker images with 
some minor alterations.

* Initial creation based on Vagrant, with a plan to move to packer to create an AMI

* Godaddy update of dns requires environment to contain a production key and secret:
```
export godaddy_key=<key goes here>

export godaddy_secret=<secret key goes here>

```
