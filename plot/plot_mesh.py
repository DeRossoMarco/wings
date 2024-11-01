import os
import pandas as pd
import re
import matplotlib.pyplot as plt

# Directory di partenza
base_dir = 'mesh'

# Dizionario per salvare i risultati
results = {'Nx': [], 'Ny': [], 'Cd_mean': [], 'Cl_mean': []}

# Definiamo i nomi delle colonne manualmente in base al file di esempio
column_names = [
    "Time", "Cd", "Cd(f)", "Cd(r)", "Cl", "Cl(f)", "Cl(r)",
    "CmPitch", "CmRoll", "CmYaw", "Cs", "Cs(f)", "Cs(r)"
]

# Funzione per estrarre i dati e calcolare le medie
def process_file(filepath):
    # Leggiamo il file specificando i nomi delle colonne e il separatore
    data = pd.read_csv(filepath, sep=r'\s+', comment='#', names=column_names, skiprows=9)
    
    # Verifichiamo la presenza di Cd e Cl e calcoliamo la media
    if 'Cd' in data.columns and 'Cl' in data.columns:
        Cd_mean = data['Cd'].mean()
        Cl_mean = data['Cl'].mean()
        return Cd_mean, Cl_mean
    else:
        return None, None

# Navigazione della struttura di cartelle
for folder in os.listdir(base_dir):
    if folder.startswith("postProcessing_"):
        # Estrazione di Nx e Ny dal nome della cartella
        match = re.search(r'postProcessing_(\d+)_(\d+)', folder)
        if match:
            Nx, Ny = int(match.group(1)), int(match.group(2))
            
            # Costruzione del percorso del file coefficient.dat
            coeff_path = os.path.join(base_dir, folder, 'forceCoeffs', '1', 'coefficient.dat')
            if os.path.isfile(coeff_path):
                Cd_mean, Cl_mean = process_file(coeff_path)
                if Cd_mean is not None and Cl_mean is not None:
                    # Salviamo i risultati
                    results['Nx'].append(Nx)
                    results['Ny'].append(Ny)
                    results['Cd_mean'].append(Cd_mean)
                    results['Cl_mean'].append(Cl_mean)

# Conversione dei risultati in DataFrame per visualizzazione e ordinamento
df_results = pd.DataFrame(results)

# Ordinamento in base a Nx e Ny
df_results = df_results.sort_values(by=['Nx', 'Ny']).reset_index(drop=True)
df_results['Nx_Ny'] = df_results['Nx'].astype(str) + '_' + df_results['Ny'].astype(str)

# Creiamo i subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot Cd
ax1.plot(df_results['Nx_Ny'], df_results['Cd_mean'], label='Cd', color='orange', marker='o')
ax1.set_ylabel('Cd')
ax1.set_title('Cdin function of domain subdivision')
ax1.grid(True)
ax1.legend()

# Plot Cl
ax2.plot(df_results['Nx_Ny'], df_results['Cl_mean'], label='Cl', color='green', marker='o')
ax2.set_xlabel('Nx_Ny')
ax2.set_ylabel('Cl')
ax2.set_title('Clin function of domain subdivision')
ax2.grid(True)
ax2.legend()

# Mostriamo il grafico con un layout ottimizzato
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
