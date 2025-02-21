import pandas as pd
import matplotlib.pyplot as plt

# Read data from error.csv
df = pd.read_csv("error.csv")

# Create a new index combining seed and method
df['seed-method'] = df['seed'].astype(str) + '-' + df['method'].astype(str)

# Define plot settings
plot_configs = {
    "p": "Error Pressure (error_p)",
    "wallShearStress:0": "Wall Shear Stress 0",
    "wallShearStress:1": "Wall Shear Stress 1",
    "wallShearStress:2": "Wall Shear Stress 2",
}

# Loop through each error column and plot separately
for column, title in plot_configs.items():
    plt.figure(figsize=(8, 5))
    plt.plot(df['seed-method'], df[column], marker='o', linestyle='-', label=column)
    
    # Labels and formatting
    plt.xlabel("Seed-Method")
    plt.ylabel("Error Value")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save and close plot
    filename = f"{column}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

print("Plots saved successfully!")
