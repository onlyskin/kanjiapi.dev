#!/bin/bash
set -e
set -x
ZONE=kanjiapi-dev-zone

echo $ZONE
echo $CERTBOT_DOMAIN
echo $CERTBOT_VALIDATION

gcloud --project=kanjiapi dns record-sets transaction start -z=$ZONE
gcloud --project=kanjiapi dns record-sets transaction add -z=$ZONE \
    --name="_acme-challenge.$CERTBOT_DOMAIN." \
    --type=TXT \
    --ttl=5 $CERTBOT_VALIDATION
gcloud --project=kanjiapi dns record-sets transaction execute -z=$ZONE
sleep 120

