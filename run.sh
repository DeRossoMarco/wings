#!/bin.bash
#$ -cwd                 # workingDirectory
#$ -j y
#$ -N wings
#$ -M marco.derosso@mail.polimi.it
#$ -m e
#$ -S /bin/bash
#$ -q all.q             # queueName
#$ -pe mpi 32           # cpuNumber
#$ -l h_rt=10:00:00

module use /software/spack/spack/share/spack/modules/linux-rocky8-sandybridge/
module load openfoam

# #!/bin/bash
localDir='/global-scratch/mderosso/wings'

decompDict="-decomposeParDict system/decomposeParDict.32"

cp -r 0.orig 0

touch wings.foam

cp -rf system/simple/ system

runApplication blockMesh

runApplication surfaceFeatureExtract

runApplication $decompDict decomposePar

# Using distributedTriSurfaceMesh?
if foamDictionary -entry geometry -value system/snappyHexMeshDict | \
   grep -q distributedTriSurfaceMesh
then
    echo "surfaceRedistributePar does not need to be run anymore"
    echo " - distributedTriSurfaceMesh will do on-the-fly redistribution"
fi

runParallel $decompDict snappyHexMesh -overwrite

runParallel $decompDict extrudeMesh

runParallel $decompDict transformPoints -translate "(0 0 -1)"

runParallel $decompDict topoSet

runParallel $decompDict checkMesh -writeFields '(nonOrthoAngle)' -constant

#- For non-parallel running: - set the initial fields
# restore0Dir

#- For parallel running: set the initial fields
restore0Dir -processor

runParallel $decompDict potentialFoam -writephi -writePhi

runParallel $decompDict $(getApplication)

# runParallel $decomposeDict renumberMesh -overwrite

cp -rf system/pimple/ system

runParallel $decompDict $(getApplication)

runApplication reconstructParMesh -constant

runApplication reconstructPar

#------------------------------------------------------------------------------

