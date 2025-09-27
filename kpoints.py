# generate_kpoints.py
"""
Generate 12x12x12 k-points for Wannier90 .win file
Output matches the developers' style: fractional coordinates with 8 decimal places.
"""

import numpy as np

# Grid size
nx = ny = nz = 12

# Weight for each k-point (1/(12^3))
weight = 1.0 / (nx * ny * nz)

kpoints = []

# Loop over all fractional coordinates
for i in range(nx):
    for j in range(ny):
        for k in range(nz):
            kx = i / nx
            ky = j / ny
            kz = k / nz
            kpoints.append((kx, ky, kz))

# Print in Wannier90 format
print("begin kpoints")
for kx, ky, kz in kpoints:
    print(f" {kx:.8f} {ky:.8f} {kz:.8f} 1.562500e-02 ")
print("end kpoints")

print(f"\nTotal k-points: {len(kpoints)}")
print(f"Each weight: {weight:.8e}")
