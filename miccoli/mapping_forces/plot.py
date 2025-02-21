import pandas as pd
import matplotlib.pyplot as plt

# Read data from error.csv
df = pd.read_csv("error.csv")

# Define plot settings
plot_configs = {
    "p": "Error Pressure",
    "wallShearStress:0": "Wall Shear Stress 0",
    "wallShearStress:1": "Wall Shear Stress 1",
    "wallShearStress:2": "Wall Shear Stress 2",
}

# Convert 'seed' to numeric for proper sorting
df['seed'] = df['seed'].astype(float)
df = df.sort_values(by='seed')

# Loop through each error column and plot separately
for column, title in plot_configs.items():
    plt.figure(figsize=(8, 5))

    # Filter data by method
    for method in ["Center", "Nodes"]:
        subset = df[df["method"] == method]
        plt.plot(subset["seed"], subset[column], marker='o', linestyle='-', label=method)

    # Labels and formatting
    plt.xlabel("Seed")
    plt.ylabel("Error Value")
    plt.title(title)
    plt.xticks(df["seed"].unique(), labels=[f"{s:.4f}" for s in df["seed"].unique()])
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save and close plot
    filename = f"{column}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

print("Plots saved successfully!")
