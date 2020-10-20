#!/bin/bash
set -e

DATE=$(date '+%Y-%m-%d')

certbot certonly \
  --agree-tos \
  --manual \
  --email s.szreter@gmail.com \
  -d kanjiapi.dev \
  -d kai.kanjiapi.dev \
  --expand \
  --preferred-challenges=dns \
  --config-dir=/tmp/certbot/config \
  --work-dir=/tmp/certbot/work \
  --logs-dir=/tmp/certbot/logs \
  --manual-public-ip-logging-ok \
  --manual-auth-hook ./scripts/certbot_auth_hook.sh \
  --manual-cleanup-hook ./scripts/certbot_cleanup.sh \
  -n

gcloud --project=onlyskin-dev compute ssl-certificates create kanjiapi-dev-ssl-certificate-$DATE \
    --certificate=/tmp/certbot/config/live/kanjiapi.dev/fullchain.pem \
    --private-key=/tmp/certbot/config/live/kanjiapi.dev/privkey.pem

# run this file, then run the one in ../onlskin.dev/scripts/update_cert.sh which actually sets the certificates on gcloud
