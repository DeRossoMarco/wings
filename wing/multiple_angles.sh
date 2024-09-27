#!/bin/bash
#$ -N multiple_angle
#$ -l h_rt=20:00:00

CORES=$1
MAX_ANGLE=$2
ANGLE_STEP=$3
SPEED=$4

mkdir -p ../../multiple_angles

# Output preparation
file="1/coefficient.dat"
output_file="cdcl.txt"
if [ -e "$output_file" ]
then
    rm "$output_file"
fi

for (( ANGLE=-$MAX_ANGLE; ANGLE<=$MAX_ANGLE; ANGLE+=$ANGLE_STEP )); do
    echo "##### Running simulation with angle=$ANGLE #####"

    # Run
    cp -f 0.orig/include/initialConditions.orig 0.orig/include/initialConditions
    sed -i "s/SPEED/$SPEED/" 0.orig/include/initialConditions
    sed -i "s/ANGLE/$ANGLE/" 0.orig/include/initialConditions
    ./cluster_run.sh $CORES

    # Copy results
    cp -rf postProcessing ../../multiple_angles/postProcessing_${ANGLE}
    ./Allclean

    # Write mean
    cd ../../multiple_angles/postProcessing_${ANGLE}/forceCoeffs
    total_lines=$(wc -l < "$file")
    lines_to_process=100
    start_line=$((total_lines - lines_to_process + 1))
    data=$(tail -n "$lines_to_process" "$file" | awk '{print $2, $5}')
    min_cd=$(echo "$data" | awk '{print $1}' | sort -n | head -n 1)
    max_cd=$(echo "$data" | awk '{print $1}' | sort -n | tail -n 1)
    min_cl=$(echo "$data" | awk '{print $2}' | sort -n | head -n 1)
    max_cl=$(echo "$data" | awk '{print $2}' | sort -n | tail -n 1)
    mean_cd=$(awk "BEGIN {print ($min_cd + $max_cd) / 2}")
    mean_cl=$(awk "BEGIN {print ($min_cl + $max_cl) / 2}")
    cd ../..
    echo "$ANGLE $mean_cd $mean_cl" >> "$output_file"
    cd ../wings/wing
done

./Allclean -a
