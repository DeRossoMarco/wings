import pandas as pd

input_file = 'forces.csv'
output_file = 'forces_short.csv'

df = pd.read_csv(input_file)

mask = (df['p'] != 0) | (df[['wallShearStress:0', 'wallShearStress:1', 'wallShearStress:2']] != 0).any(axis=1)

filtered_df = df[mask]

filtered_df.to_csv(output_file, index=False)