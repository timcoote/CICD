container_loc="/etc/gitlab"
local_conf="docker/service/gitlab/config/"

container="vagrant_gitlab_1"

sudo cp install.certbot get-gitlab-cert $local_conf

docker exec $container mkdir -p mkdir -p /var/www/public/letsencrypt

docker exec $container chown -R gitlab-www /var/www/public

sudo patch $local_conf/gitlab.rb < patch1
 
docker exec $container gitlab-ctl reconfigure
docker exec $container gitlab-ctl restart

docker exec $container sh -x $container_loc/install.certbot
docker exec $container sh -x $container_loc/get-gitlab-cert

sudo patch $local_conf/gitlab.rb < patch2


docker exec $container gitlab-ctl reconfigure
docker exec $container gitlab-ctl restart
