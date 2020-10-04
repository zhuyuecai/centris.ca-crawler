#!/bin/bash
date=$(date '+%Y-%m-%d')
regions=("mont-royal" "montreal-lasalle" "montreal-lachine" "dorval" "beaconsfield" "chateauguay" "saint-lambert-monteregie")
property_types=("houses" "condos")


for i in "${property_types[@]}"
do 
    for j in "${regions[@]}"
    do
        echo ${j}
        python output_ETL.py "${i}_${j}_output_file" "${j}" montreal "${date}"
        python summarize.py "${date}_${i}_${j}_output_file"
    done
done
