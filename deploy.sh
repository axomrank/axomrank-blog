#!/usr/bin/env bash
# Build the blog and publish _site to the gh-pages branch (used until the
# GitHub Actions workflow in ci/pages.yml is enabled; see README).
set -euo pipefail
BASE_URL="${BASE_URL:-https://axomrank.github.io/axomrank-blog}"
python3 build.py --base-url "$BASE_URL"
cd _site
git init -q -b gh-pages
git add -A
git -c user.name="$(git -C .. config user.name)" -c user.email="$(git -C .. config user.email)" commit -q -m "Deploy $(git -C .. rev-parse --short HEAD)"
git push -q -f "$(git -C .. remote get-url origin)" gh-pages
rm -rf .git
echo "deployed to $BASE_URL"
