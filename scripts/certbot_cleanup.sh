#!/bin/bash
set -e
ZONE=kanjiapi-dev-zone

gcloud --project=kanjiapi dns record-sets transaction start -z=$ZONE
gcloud --project=kanjiapi dns record-sets transaction remove -z=$ZONE \
    --name="_acme-challenge.$CERTBOT_DOMAIN." \
    --type=TXT \
    --ttl=5 $CERTBOT_VALIDATION
gcloud --project=kanjiapi dns record-sets transaction execute -z=$ZONE
sleep 120

