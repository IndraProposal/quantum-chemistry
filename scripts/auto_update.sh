#!/bin/bash
set -e

latest_commit=$(git log -1 --pretty=format:%H)
latest_msg=$(git log -1 --pretty=format:%s)

mkdir -p updates
log_file="updates/update_log.md"

echo "- $(date -u +"%Y-%m-%d %H:%M:%S") UTC - last commit $latest_commit: $latest_msg" >> "$log_file"

git add "$log_file"

git commit -m "Automated update" && git push || echo "No changes to commit"

