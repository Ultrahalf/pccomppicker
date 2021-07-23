#!/bin/sh
# Change the path if needed

node ~/pccp/src/node/utils/preScraping.js >/dev/null 2>&1
FILES=$(find ~/pccp/src/node -maxdepth 1 -type f -name "*.js")

for SCRAPE in $FILES
do
  node $SCRAPE >/dev/null 2>&1
done

node ~/pccp/src/node/utils/deleteItems.js >/dev/null 2>&1
node ~/pccp/src/node/utils/xUpdate.js >/dev/null 2>&1
