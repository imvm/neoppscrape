#!/bin/bash
# Usage: remove all utility bills pdf file password 
shopt -s nullglob
rm -rf ../shtmls
mkdir ../shtmls

for f in ../data/*.csv
do
	echo "Converting csv to shtml - $f"
	filename=$(basename "$f")
	filename="${filename%.*}"
    awk -f ./htmlconvert.awk $f > ../shtmls/${filename}.shtml
done
