#!/bin/sh

while [ 1 ] ; do
	python3 ./assign.py >> outfile || (echo 'FAILED'; break)
done
