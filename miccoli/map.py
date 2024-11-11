import vtk
import numpy as np

# Load OpenFOAM mesh in binary .vtp format
openfoam_reader = vtk.vtkXMLPolyDataReader()
openfoam_reader.SetFileName("wing.vtp")
openfoam_reader.Update()
openfoam_mesh = openfoam_reader.GetOutput()

# Define transformations: translations, rotations, and scales
transform = vtk.vtkTransform()

# Apply rotation (in degrees)
transform.RotateX(90)
transform.RotateY(90)
transform.RotateZ(0)

# Apply scaling (for the geometry, not the stresses)
transform.Scale(100.0487, 100.2862, 30)

# Apply translation (for the geometry, not the stresses)
transform.Translate(-0.49489, -0.02355, -0.1666)

# Apply the transformation to the OpenFOAM mesh
transform_filter = vtk.vtkTransformPolyDataFilter()
transform_filter.SetInputData(openfoam_mesh)
transform_filter.SetTransform(transform)
transform_filter.Update()
transformed_mesh = transform_filter.GetOutput()

# Load Fusion360 mesh in .obj format
fusion_reader = vtk.vtkOBJReader()
fusion_reader.SetFileName("wing.obj")
fusion_reader.Update()
fusion_mesh = fusion_reader.GetOutput()

# Use vtkProbeFilter to resample OpenFOAM data onto Fusion360 mesh
probe = vtk.vtkProbeFilter()
probe.SetInputData(fusion_mesh)
probe.SetSourceData(transformed_mesh)
probe.SetComputeTolerance(False)
probe.SetTolerance(0.15)
probe.Update()
resampled_mesh = probe.GetOutput()

# Rotate the stress vector components
stress_array = resampled_mesh.GetPointData().GetArray("wallShearStress")
if stress_array:
    # Extract rotation matrix from transform
    rotation_matrix = vtk.vtkMatrix4x4()
    transform.GetMatrix(rotation_matrix)
    
    # Convert rotation part of matrix to numpy array for easy vector rotation
    rotation_np = np.array([[rotation_matrix.GetElement(i, j) for j in range(3)] for i in range(3)])
    
    # Loop through each vector and apply the rotation matrix
    for i in range(stress_array.GetNumberOfTuples()):
        original_stress = np.array(stress_array.GetTuple(i))
        rotated_stress = rotation_np.dot(original_stress)  # Rotate vector
        stress_array.SetTuple(i, rotated_stress)           # Update with rotated vector

# Save the resampled mesh with rotated stress data
writer = vtk.vtkXMLPolyDataWriter()
writer.SetFileName("forces.vtp")
writer.SetInputData(resampled_mesh)
writer.Write()
