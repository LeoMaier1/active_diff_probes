import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from spicelib import RawRead
import os

plt.rcParams.update({
    "font.family": "serif", 
    "font.size": 11, 
    "axes.labelsize": 11, 
    "legend.fontsize": 10, 
    "xtick.labelsize": 10, 
    "ytick.labelsize": 10, 
    "lines.linewidth": 1.5
})
formatter = ticker.FuncFormatter(lambda value, _position: f"{value:g}".replace(".", ","))
width = 15.0 / 2.54

if not os.path.exists('bilder'):
    os.makedirs('bilder')

raw_filename = "../ltspice/mcdiffamp.raw" 

try:
    print(f"Lese Monte-Carlo Daten aus {raw_filename}...")
    ltr = RawRead(raw_filename)
except FileNotFoundError:
    print(f"Fehler: Datei nicht gefunden!")
    exit()

steps = ltr.get_steps()
num_steps = len(steps)
print(f"Gefundene Monte-Carlo-Durchläufe: {num_steps}")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(width, width), sharex=True)

freq = np.real(ltr.get_trace('frequency').get_wave(0))

print("Zeichne Graphen...")

for step in range(num_steps):
    v_out = ltr.get_trace('V(uout)').get_wave(step)
    
    cmrr_db = 20 * np.log10((1/150) / np.abs(v_out))
    
    phase_deg = np.unwrap(np.angle(v_out)) * (180 / np.pi)
    
    ax1.semilogx(freq, cmrr_db, color='black', alpha=0.3, ls='-')
    ax2.semilogx(freq, phase_deg, color='black', alpha=0.3, ls='-')

ax1.set_ylabel(r'CMRR in dB')
ax1.grid(True, which="both", color='gray', ls=":", alpha=0.7)
ax1.yaxis.set_major_formatter(formatter)

ax2.set_xlabel(r'$f$ in Hz')
ax2.set_ylabel(r'Phase $\varphi$ in $^\circ$')
ax2.grid(True, which="both", color='gray', ls=":", alpha=0.7)
ax2.yaxis.set_major_formatter(formatter)

fig.tight_layout()

plt.savefig('bilder/plot_montecarlo.pdf', format="pdf", bbox_inches="tight")
print("Bild gespeichert unter: bilder/plot_montecarlo.pdf")
plt.show()