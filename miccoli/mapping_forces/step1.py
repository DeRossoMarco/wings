import vtk
import numpy as np

# Load OpenFOAM mesh in binary .vtp format
openfoam_reader = vtk.vtkXMLPolyDataReader()
openfoam_reader.SetFileName("wing.vtp")
openfoam_reader.Update()
openfoam_mesh = openfoam_reader.GetOutput()

# Load Fusion360 mesh in .obj format
fusion_reader = vtk.vtkOBJReader()
fusion_reader.SetFileName("wing.obj")
fusion_reader.Update()
fusion_mesh = fusion_reader.GetOutput()

# Use vtkProbeFilter to resample OpenFOAM data onto Fusion360 mesh
probe = vtk.vtkProbeFilter()
probe.SetInputData(fusion_mesh)
probe.SetSourceData(openfoam_mesh)
probe.SetComputeTolerance(False)
probe.SetTolerance(0.005)
probe.Update()
resampled_mesh = probe.GetOutput()

# Save the resampled mesh with rotated stress data
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("step1out.vtp")
writer.SetInputData(resampled_mesh)
writer.Write()
