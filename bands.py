import numpy as np
import matplotlib.pyplot as plt

Efermi = 5.432  # replace with Fermi energy from scf/relax
bands = []
with open("si.bands.gnu") as f:
    block = []
    for line in f:
        if line.strip() == "":
            if block:
                bands.append(np.array(block))
                block = []
        else:
            k, E = map(float, line.split()[:2])
            block.append([k, E])
    if block:
        bands.append(np.array(block))

plt.figure(figsize=(7,6))
for band in bands:
    plt.plot(band[:,0], band[:,1] - Efermi, 'b-')

plt.axhline(0.0, color='k', linestyle='--', linewidth=0.8)

# Example k-point positions (replace with your path!)
sym_points = [0, 1.0, 2.0, 3.0]   # x-coordinates where high-symmetry points occur
labels     = [r'$\Gamma$', 'X', 'L', r'$\Gamma$']

for x in sym_points:
    plt.axvline(x, color='k', linestyle='-', linewidth=0.5)

plt.xticks(sym_points, labels)
plt.ylabel("Energy (eV, relative to $E_F$)")
plt.title("Si Band Structure")
plt.tight_layout()
plt.savefig("si_bands_with_labels.png", dpi=300)
plt.show()
