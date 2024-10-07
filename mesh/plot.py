import numpy as np
import matplotlib.pyplot as plt

# Load data from the files
real_data = np.loadtxt('cdcl_target.txt')
simulated_data = np.loadtxt('cdcl.txt')

# Extract columns: angle (alpha), Cd, and Cl
alpha_real, cd_real, cl_real = real_data[:, 0], real_data[:, 1], real_data[:, 2]
alpha_sim, cd_sim, cl_sim = simulated_data[:, 0], simulated_data[:, 1], simulated_data[:, 2]

# Create a figure and axis for Cd plot
plt.figure(figsize=(12, 6))

# Plot Cd vs alpha
plt.subplot(1, 2, 1)
plt.plot(alpha_real, cd_real, label='Real Cd', color='blue', marker='o')
plt.plot(alpha_sim, cd_sim, label='Simulated Cd', color='orange', marker='x')
plt.xlabel(r'Angle $\alpha$ (degrees)')
plt.ylabel(r'$C_d$ (Drag Coefficient)')
plt.title('Drag Coefficient vs Angle')
plt.legend()
plt.grid(True)

# Plot Cl vs alpha
plt.subplot(1, 2, 2)
plt.plot(alpha_real, cl_real, label='Real Cl', color='green', marker='o')
plt.plot(alpha_sim, cl_sim, label='Simulated Cl', color='red', marker='x')
plt.xlabel(r'Angle $\alpha$ (degrees)')
plt.ylabel(r'$C_l$ (Lift Coefficient)')
plt.title('Lift Coefficient vs Angle')
plt.legend()
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
