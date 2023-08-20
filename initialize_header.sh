#!/bin/sh

echo "Initializing Headers"

for f in scraped-data/*
do 
    cp header.csv $f;
done

echo "\033[0;32m[DONE] Initialized Heraders"