#!/bin/sh
# Change the path if needed

node ../node/utils/preScraping.js >/dev/null 2>&1
FILES=$(find ../node -maxdepth 1 -type f -name "*.js")

for SCRAPE in $FILES
do
  node $SCRAPE >/dev/null 2>&1
done

node ../node/utils/deleteItems.js >/dev/null 2>&1
node ../node/utils/xUpdate.js >/dev/null 2>&1
