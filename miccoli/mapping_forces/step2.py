import re
import csv
import numpy as np
from scipy.spatial import KDTree

def load_csv_data(csv_file):

    coordinates = []
    forces = []
    pressures = []

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Read the header and identify column indices
        header = next(csv_reader)
        points_indices = [header.index('Points:0'), header.index('Points:1'), header.index('Points:2')]
        shear_indices = [header.index('wallShearStress:0'), header.index('wallShearStress:1'), header.index('wallShearStress:2')]
        pressure_index = header.index('p')
        
        # Read the data rows
        for row in csv_reader:
            coordinates.append([float(row[i]) for i in points_indices])
            forces.append([float(row[i]) for i in shear_indices])
            pressures.append(float(row[pressure_index]))

    coordinates = np.array(coordinates)
    forces = np.array(forces)
    pressures = np.array(pressures)

    # Build a KDTree for fast nearest-neighbor lookup
    kdtree = KDTree(coordinates)
    
    return kdtree, forces, pressures

def find_nearest_data(kdtree, forces, pressures, face_center):
    _, index = kdtree.query(face_center)
    return pressures[index], forces[index]

def parse_inp(file_path, kdtree, forces, pressures):

    data = {"s1": [], "s2": [], "s3": [], "s4": []}
    nodes = {"idx": [], "x": [], "y": [], "z": []}
    elements = {"idx": [], "n1": [], "n2": [], "n3": [], "n4": []}

    face_map = {
        "1": ["n1", "n2", "n3"],
        "2": ["n1", "n2", "n4"],
        "3": ["n2", "n3", "n4"],
        "4": ["n1", "n3", "n4"]
    }
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    i = 0
    new_lines = []

    seed = 0.01
    #method = "Center"
    method = "Nodes"

    while i < len(lines):
        line = lines[i].strip().lower()

        if line.startswith("** part instance: wing-2"):
            new_lines.append(lines[i])
            i += 1
            new_lines.append(lines[i])
            i += 1
            new_lines.append(lines[i])
            i += 1

            # Read nodes
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(float, re.findall(r'-?\d+\.\d+|-?\d+', lines[i])))
                nodes["idx"].append(numbers[0])
                nodes["x"].append(float(numbers[1]))
                nodes["y"].append(float(numbers[2]))
                nodes["z"].append(float(numbers[3]))
                new_lines.append(lines[i])
                i += 1
            new_lines.append(lines[i])
            i += 1

            # Read elements
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(int, re.findall(r'\d+', lines[i])))
                elements["idx"].append(numbers[0])
                elements["n1"].append(numbers[1])
                elements["n2"].append(numbers[2])
                elements["n3"].append(numbers[3])
                elements["n4"].append(numbers[4])
                new_lines.append(lines[i])
                i += 1
            continue
        
        if line.startswith("*elset, elset=_external_s1"):
            i += 1
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(int, re.findall(r'\d+', lines[i])))
                for number in numbers:
                    new_lines.append(f"*Surface, type=ELEMENT, name=S_{number}_1\n")
                    new_lines.append(f" {number}, S1\n")
                data["s1"].extend(numbers)
                i += 1
            continue

        if line.startswith("*elset, elset=_external_s2"):
            i += 1
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(int, re.findall(r'\d+', lines[i])))
                for number in numbers:
                    new_lines.append(f"*Surface, type=ELEMENT, name=S_{number}_2\n")
                    new_lines.append(f" {number}, S2\n")
                data["s2"].extend(numbers)
                i += 1
            continue
        
        if line.startswith("*elset, elset=_external_s3"):
            i += 1
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(int, re.findall(r'\d+', lines[i])))
                for number in numbers:
                    new_lines.append(f"*Surface, type=ELEMENT, name=S_{number}_3\n")
                    new_lines.append(f" {number}, S3\n")
                data["s3"].extend(numbers)
                i += 1
            continue
        
        if line.startswith("*elset, elset=_external_s4"):
            i += 1
            while i < len(lines) and not lines[i].startswith("*"):
                numbers = list(map(int, re.findall(r'\d+', lines[i])))
                for number in numbers:
                    new_lines.append(f"*Surface, type=ELEMENT, name=S_{number}_4\n")
                    new_lines.append(f" {number}, S4\n")
                data["s4"].extend(numbers)
                i += 1
            continue
        
        if line.startswith("*surface, type=element, name=external"):
            i += 1
            while i < len(lines) and not lines[i].startswith("*"):
                i += 1
            continue

        if line.startswith("** name: load"):
            i += 2
            while i < len(lines) and not lines[i].startswith("*"):
                i += 1

            elements_idx_map = {val: idx for idx, val in enumerate(elements["idx"])}
            nodes_idx_map = {val: idx for idx, val in enumerate(nodes["idx"])}

            total_pressure_force = 0.0
            total_shear_force = np.array([0.0, 0.0, 0.0])
            
            for k in range(4):

                idata = data[f"s{k+1}"]

                for number in idata:

                    index = elements_idx_map[number]
                    element = {key: values[index] for key, values in elements.items()}
                    nodes_indices = face_map[str(k+1)]
                    nodes_indices = [element[node] for node in nodes_indices]

                    x = np.array([nodes["x"][nodes_idx_map[node]] for node in nodes_indices])
                    y = np.array([nodes["y"][nodes_idx_map[node]] for node in nodes_indices])
                    z = np.array([nodes["z"][nodes_idx_map[node]] for node in nodes_indices])

                    face_center = np.array([np.mean(x), np.mean(y), np.mean(z)])

                    v1 = np.array([x[1] - x[0], y[1] - y[0], z[1] - z[0]])
                    v2 = np.array([x[2] - x[0], y[2] - y[0], z[2] - z[0]])
                    face_area = 0.5 * np.linalg.norm(np.cross(v1, v2))
                    
                    if method == "Center":
                        pressure, force = find_nearest_data(kdtree, forces, pressures, face_center)
                    
                    elif method == "Nodes":
                        pressure1, force1 = find_nearest_data(kdtree, forces, pressures, np.array([x[0], y[0], z[0]]))
                        pressure2, force2 = find_nearest_data(kdtree, forces, pressures, np.array([x[1], y[1], z[1]]))
                        pressure3, force3 = find_nearest_data(kdtree, forces, pressures, np.array([x[2], y[2], z[2]]))

                        pressure = (pressure1 + pressure2 + pressure3) / 3
                        force = (force1 + force2 + force3) / 3
                    
                    pressure_force = pressure * face_area
                    shear_force = force * face_area

                    total_pressure_force += pressure_force
                    total_shear_force += shear_force

                    f_norm = np.linalg.norm(force)
                    
                    new_lines.append(f"** Name: P_{number}_{k+1}   Type: Pressure\n")
                    new_lines.append(f"*Dsload\n")
                    new_lines.append(f"S_{number}_{k+1}, P, {pressure}\n")
                    if f_norm > 0:
                        x, y, z = force / f_norm
                        new_lines.append(f"** Name: S_{number}_{k+1}   Type: Surface traction\n")
                        new_lines.append(f"*Dsload\n")
                        new_lines.append(f"S_{number}_{k+1}, TRSHR, {f_norm}, {-x}, {-y}, {-z}\n")
            
            continue
        
        new_lines.append(lines[i])
        i += 1

    with open("out.inp", 'w') as file:
        file.writelines(new_lines)

    with open("integrate.csv", mode="r") as file:
        reader = csv.reader(file)
        header = next(reader)
        first_row = next(reader)
        input_values = np.array([float(val) for val in first_row])
        
    pressure_diff = abs(total_pressure_force - input_values[0])
    shear_diff = np.abs(total_shear_force - input_values[1:4])

    with open("error.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([method] + [seed] + [pressure_diff] + shear_diff.tolist())
    
    return data

if __name__ == "__main__":

    csv_file = "forces.csv"
    kdtree, forces, pressures = load_csv_data(csv_file)

    inp_file = "in.inp"
    data = parse_inp(inp_file, kdtree, forces, pressures)