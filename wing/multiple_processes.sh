#!/bin/bash
#$ -N multiple_processes
#$ -l h_rt=20:00:00

MAX_PROCESSES=$1

rm -rf ../../multiple_cores && mkdir -p ../../multiple_cores

for (( CORES=1; CORES<=$MAX_PROCESSES; CORES*=2 )) do
        echo "##### Running simulation with $CORES cores #####"
        cp -f wing/system/decomposeParDict.orig wing/system/decomposeParDict
        sed -i "s/CORES/$CORES/" wing/system/decomposeParDict
        cd wing
        ./cluster_run.sh
        # Copy results
        cp -rf postProcessing ../../multiple_cores/postProcessing_${CORES}
        ./Allclean
        cd ..
    done

./Allclean -a
