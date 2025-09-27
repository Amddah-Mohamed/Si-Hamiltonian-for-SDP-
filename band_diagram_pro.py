import numpy as np
import matplotlib.pyplot as plt

# Create the visualization
fig, ax = plt.subplots(figsize=(10, 8))

# Define high symmetry points in the Brillouin zone (simplified for Si)
high_sym_points = ['Γ', 'X', 'W', 'K', 'Γ', 'L', 'W', 'L']
x_ticks = [0, 1, 2, 3, 4, 5, 6, 7]
x_tick_positions = [0, 1, 2, 3, 4, 5, 6, 7]

# Generate some sample band data (this would normally come from DFT calculations)
x = np.linspace(0, 7, 300)

# Valence bands (below Fermi level)
valence_1 = -2 - 3*np.sin(0.8*x) - 0.5*np.cos(1.3*x) - 18
valence_2 = -1 - 2*np.sin(0.7*x) - 0.3*np.cos(1.1*x) - 18
valence_3 = -0.5 - 1.5*np.sin(0.6*x) - 0.2*np.cos(0.9*x) - 18

# Conduction bands (above Fermi level)
conduction_1 = 1 + 1.5*np.sin(0.7*x) + 0.4*np.cos(1.2*x) - 2
conduction_2 = 2 + 2*np.sin(0.8*x) + 0.6*np.cos(1.4*x) - 2
conduction_3 = 4 + 2.5*np.sin(0.9*x) + 0.8*np.cos(1.6*x) - 2

# Plot valence bands
ax.plot(x, valence_1, 'b-', linewidth=1.5, label='Valence Bands')
ax.plot(x, valence_2, 'b-', linewidth=1.5)
ax.plot(x, valence_3, 'b-', linewidth=1.5)

# Plot conduction bands
ax.plot(x, conduction_1, 'r-', linewidth=1.5, label='Conduction Bands')
ax.plot(x, conduction_2, 'r-', linewidth=1.5)
ax.plot(x, conduction_3, 'r-', linewidth=1.5)

# Add Fermi level
ax.axhline(y=0, color='k', linestyle='--', linewidth=1, label='Fermi Level ($E_F$)')

# Set labels and title
ax.set_xlabel('Wave Vector', fontsize=12)
ax.set_ylabel('Energy (eV, relative to $E_F$)', fontsize=12)
ax.set_title('Silicon (Si) Band Structure', fontsize=14, fontweight='bold')

# Set x-ticks at high symmetry points
ax.set_xticks(x_tick_positions)
ax.set_xticklabels(high_sym_points)

# Set y-axis limits and ticks
ax.set_ylim(-25, 10)
ax.set_yticks([-20, -15, -10, -5, 0, 5, 10])

# Add grid for better readability
ax.grid(True, linestyle='--', alpha=0.7)

# Add legend
ax.legend(loc='upper right', frameon=True)

# Add text annotations for band gap
ax.annotate('Indirect Band Gap (~1.1 eV)', 
            xy=(3.5, 0.5), xytext=(4, 3),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            fontsize=10, ha='center')

# Adjust layout to prevent clipping of labels
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig('si_bands_with_labels.png', dpi=300, bbox_inches='tight')

print("Band structure plot saved as 'si_bands_with_labels.png'")

# If you want to also display the plot (if in an interactive environment)
# plt.show()
