#!/bin/bash
#
# Build the book from the current checkout and publish it as the /docs
# section of the production site.
#
# Called by r2lab-embedded/services/run-updates.sh after it has moved this
# repo to the latest origin commit; can also be run by hand to force a redeploy.
# The git update itself is NOT done here, since resetting a repo under a
# running script is unsafe.
#
# Notes
# - the book is built with BASE_URL=/docs (see the build:prod script in
#   package.json), and published as static files in $PUBLISH_PATH, so that
#   neither django nor any service needs a restart
# - nginx is not touched: its configuration is not part of this repo; it
#   must map /docs/ onto $PUBLISH_PATH, e.g.
#     location /docs/ { alias /var/www/r2lab-docs/; }
# - the build needs node/npm and uv on the host (the diffs between successive
#   tutorial steps are generated at build time, they are not in git), and
#   network access, since the theme is downloaded from the github release
#   mentioned in myst.yml
# - _build is wiped each time, otherwise myst keeps using a cached copy of the
#   theme in _build/templates, and a new release would never be picked up
#

set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")/.."

export PATH="/root/.local/bin:$PATH"

# overridable, to test the script without touching the real site
PUBLISH_PATH=${PUBLISH_PATH:-/var/www/r2lab-docs}

rm -rf _build
npm ci
npm run build:prod

# sanity check, so that a broken build never wipes the published site
[[ -f _build/html/index.html ]] || { echo "update.sh: no _build/html/index.html, not publishing"; exit 1; }

mkdir -p "$PUBLISH_PATH"
rsync -ai --delete _build/html/ "$PUBLISH_PATH"/
