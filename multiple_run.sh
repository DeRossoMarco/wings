#!/bin/bash
file="coefficients.dat"
output_file="cdcl.txt"
if [ -e "$output_file" ]; then    rm "$output_file"
fi
cd wing
cp system/blockMeshDict.orig system/blockMeshDict
cp 0.orig/include/initialConditions.orig 0.orig/include/initialConditions
Nx=25
Ny=25
sed -i "s/Nx/$Nx/; s/Ny/$Ny/" system/blockMeshDict
for angle in {-20..20..5}; do
    echo "Running Allrun with angle=$angle"
    sed -i "s/angle/$angle/" 0.orig/include/initialConditions
    ./Allrun
    cp PostProcessing -r ../PostProcessing_${angle}
    cp 0.orig/include/initialConditions.orig 0.orig/include/initialConditions
    ./Allclean    
    cd ..
    cd PostProcessing_${angle}/forceCoeff
    total_lines=$(wc -l < "$file")
    lines_to_process=100
    start_line=$((total_lines - lines_to_process + 1))
    data=$(tail -n "$lines_to_process" "$file" | awk '{print $2, $5}')
    min_col2=$(echo "$data" | awk '{print $1}' | sort -n | head -n 1)
    max_col2=$(echo "$data" | awk '{print $1}' | sort -n | tail -n 1)
    min_col5=$(echo "$data" | awk '{print $2}' | sort -n | head -n 1)
    max_col5=$(echo "$data" | awk '{print $2}' | sort -n | tail -n 1)
    mean_col2=$(awk "BEGIN {print ($min_col1 + $max_col1) / 2}")    mean_col5=$(awk "BEGIN {print ($min_col4 + $max_col4) / 2}")
    cd ../..

    echo "$angle $mean_col2 $mean_col5" >> "$output_file"
    cd wing    
done
