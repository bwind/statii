#!/bin/bash -e
DEPLOY_ENV=$1
APP_NAME=statii
eval "SWARM_MANAGER=\$SWARM_MANAGER_$DEPLOY_ENV"

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
docker build -t maxwellai/$APP_NAME:$BITBUCKET_COMMIT .
docker push maxwellai/$APP_NAME:$BITBUCKET_COMMIT
ssh maxwell@${SWARM_MANAGER} << EOF
    cd dockercloud/stacks/statii
    sed -i 's/STATII_VERSION=.*$/STATII_VERSION=$BITBUCKET_COMMIT/' .env
    bash deploy.sh
EOF
