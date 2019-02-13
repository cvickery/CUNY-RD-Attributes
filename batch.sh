#! /usr/local/bin/bash

# Sample script to process a batch of query files.
for term in 1172 1179 1182 1189 1192
do echo -e "\n\nSemester $term\n============="
   ./rd-attr.py $term
done
