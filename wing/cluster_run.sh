#!/bin/bash
#$ -N single_run
#$ -l h_rt=10:00:00

CORES=$1

module use /software/spack/spack/share/spack/modules/linux-rocky8-sandybridge/
module load openfoam
. $WM_PROJECT_DIR/bin/tools/RunFunctions

#!/bin/bash
localDir="/home/meccanica/mderosso/wings/wing"

cp -r 0.orig 0
touch wings.foam
cp -rf system/simple/* system/
mkdir log

echo "Running blockMesh"
blockMesh > $localDir/log/log.blockMesh 2>&1

echo "Running surfaceFeatureExtract"
surfaceFeatureExtract > $localDir/log/log.surfaceFeatureExtract 2>&1

echo "Running decomposePar"
decomposePar > $localDir/log/log.decomposePar 2>&1

echo "Running snappyHexMesh in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES snappyHexMesh -parallel -overwrite < /dev/null > $localDir/log/log.snappyHexMesh 2>&1

echo "Running extrudeMesh in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES extrudeMesh -parallel < /dev/null > $localDir/log/log.extrudeMesh 2>&1

echo "Running transformPoints in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES transformPoints -parallel -translate "(0 0 -1)" < /dev/null > $localDir/log/log.transformPoints 2>&1

echo "Running topoSet in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES topoSet -parallel < /dev/null > $localDir/log/log.topoSet 2>&1

echo "Running checkMesh in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES checkMesh -parallel -writeFields '(nonOrthoAngle)' -constant < /dev/null > $localDir/log/log.checkMesh 2>&1

restore0Dir -processor

echo "Running potentialFoam in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES potentialFoam -parallel -writephi < /dev/null > $localDir/log/log.potentialFoam 2>&1

echo "Running simpleFoam in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES simpleFoam -parallel < /dev/null > $localDir/log/log.simpleFoam 2>&1

# runParallel $decomposeDict renumberMesh -overwrite

cp -rf system/pimple/* system/

echo "Running pimpleFoam in parallel using $CORES processes"
mpirun --hostfile machinefile.$JOB_ID -np $CORES pimpleFoam -parallel < /dev/null > $localDir/log/log.pimpleFoam 2>&1

echo "Running reconstructParMesh"
reconstructParMesh -constant > $localDir/log/log.reconstructParMesh 2>&1

echo "Running reconstructPar"
reconstructPar > $localDir/log/log.reconstructPar 2>&1

