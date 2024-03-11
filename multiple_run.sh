#!/bin/bash
#$ -cwd
#$ -j y
#$ -N wings
#$ -S /bin/bash
#$ -q all.q             # queueName
#$ -pe mpi 16           # cpuNumber
#$ -l h_rt=20:00:00

module use /software/spack/spack/share/spack/modules/linux-rocky8-sandybridge/
module load openfoam

file="1/coefficient.dat"
output_file="cdcl.txt"
if [ -e "$output_file" ]
then
    rm "$output_file"
fi
cd wing
cp system/blockMeshDict.orig system/blockMeshDict
cp 0.orig/include/initialConditions.orig 0.orig/include/initialConditions
Nx=25
Ny=25
sed -i "s/Nx/$Nx/; s/Ny/$Ny/" system/blockMeshDict
for angle in {-20..20..5}; do
    echo "Running simulation with angle=$angle"
    sed -i "s/angle/$angle/" 0.orig/include/initialConditions
    ./cluster_run.sh
    cp -r postProcessing ../postProcessing_${angle}
    cp 0.orig/include/initialConditions.orig 0.orig/include/initialConditions
    ./Allclean    
    cd ..
    cd postProcessing_${angle}/forceCoeffs
    total_lines=$(wc -l < "$file")
    lines_to_process=100
    start_line=$((total_lines - lines_to_process + 1))
    data=$(tail -n "$lines_to_process" "$file" | awk '{print $2, $5}')
    min_cd=$(echo "$data" | awk '{print $1}' | sort -n | head -n 1)
    max_cd=$(echo "$data" | awk '{print $1}' | sort -n | tail -n 1)
    min_cl=$(echo "$data" | awk '{print $2}' | sort -n | head -n 1)
    max_cl=$(echo "$data" | awk '{print $2}' | sort -n | tail -n 1)
    mean_cd=$(awk "BEGIN {print ($min_cd + $max_cd) / 2}")    mean_cl=$(awk "BEGIN {print ($min_cl + $max_cl) / 2}")
    cd ../..

    echo "$angle $mean_cd $mean_cl" >> "$output_file"
    cd wing    
done
