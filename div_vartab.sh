#!/bin/bash
while read -r l; do a=$(echo $l | cut -d' ' -f1);echo $l>dimensions_$a; done <var2.tabular
for f in dimensions_*; do cat $f | sed 's/ /\t\n/g' | sed '$s/$/ /' >$f.tabular; done
for f in dimensions_*.tabular;do cat $f | awk 'NR % 2 != 0' $f > $f.2 && mv $f.2 $f ; done
