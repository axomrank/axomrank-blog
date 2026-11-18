#!/usr/bin/env bash
# Manual fallback: build the blog and publish _site to the gh-pages branch.
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
