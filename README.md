# Build system to get Jenkins/Gitlab/Artifactory environment in AWS

* All of the components are installed on a VM, using standard(ish) docker images with 
some minor alterations.

* Initial creation based on Vagrant, with a plan to move to packer to create an AMI

* Godaddy update of dns requires environment to contain a production key and secret:
```
export godaddy_key=<key goes here>

export godaddy_secret=<secret key goes here>

```

# HTTPS Setup
Currently, the shell script `sh -x ./go` will request and install tls certificates for gitlab using
letsencrypt's cerbot. However, the mechanism is not great as the docker container is, essentially sealed.

The method is as follows:
* Run up the vagrant image in the cloud
* vagrant ssh  and cd /vagrant
* monitor /var/log/gitlab/nginx until the service can be seen to be stable (not automated)
* `sh -x ./go`: this:
**  copies a script to the container to install certbot
** creates and gets the ownership structure right on where the certificates etc are stored in the container
** patches the gitlab.rb with an http address and adds in the redirects to allow certbot challenges
to work
** reconfigures and restarts gitlab
** installs the certbot package and grabs a certificate: there are two modes for this. --staging uses
a test service, which works reliably, but does not provide a complete certficate chain. Without the flag
the letsencrypt service will throttle the rate of certificate creation. The production rate of creation is
currently 5 per 7 days.
** patch in the https configuration for nginx, reconfigure and restart.

* currently the renewal cronjob is not installed and has not been tested in this environment
