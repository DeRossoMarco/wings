import numpy as np
import importAirfoil.importAirfoil as importAirfoil
from stl import mesh

# Define constant
width = 1.0
input_file = "mesh/e554.dat"
output_file = "wingsOpenFoam/constant/triSurface/wing.stl"


# Import points

af = importAirfoil(input_file)
dim = len(af[1])


# Build vertices
vertices = np.zeros((2 * dim, 3))

for i in range(dim):
    vertices[i] = [af[0][i], af[1][i], width]
    vertices[dim + i] = [af[0][i], af[1][i], -width]


# Build faces
faces = np.zeros((dim * 2, 3), dtype=int)

for i in range(dim - 1):
    faces[2 * i] = ([i, dim + i + 1, dim + i])
    faces[2 * i + 1] = ([i, i + 1, dim + i +1])


# Create shape
wing_profile = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))

for i, f in enumerate(faces):
    for j in range(3):
        wing_profile.vectors[i][j] = vertices[f[j], :]


# Save output

wing_profile.save(output_file)
