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
    
raw_filename = "../ltspice/diffamp.raw"

try:
    print(f"Lese Daten aus {raw_filename}...")
    ltr = RawRead(raw_filename)
    traces = ltr.get_trace_names()
except FileNotFoundError:
    print(f"Fehler: Die Datei {raw_filename} wurde nicht gefunden!")
    exit()

is_transient = 'time' in traces
is_noise = 'V(onoise)' in traces or 'onoise' in traces
is_ac = 'frequency' in traces and not is_noise

# ==========================================
# 1. TRANSIENTEN-ANALYSE (.tran)
# ==========================================
if is_transient:
    print("\n=> Transienten-Analyse (.tran) erkannt!")
    
    time = ltr.get_trace('time').get_wave() * 1e9 # in ns
    v_uout = ltr.get_trace('V(uout)').get_wave()
    v_n001 = ltr.get_trace('V(n001)').get_wave()
    v_n010 = ltr.get_trace('V(n010)').get_wave()
    
    mask = (time >= 10) & (time <= 40)
    time = time[mask]
    v_uout = v_uout[mask]
    v_n001 = v_n001[mask]
    v_n010 = v_n010[mask]
    
    time = time - 10 
    
    v_uout_scaled = v_uout * 150
    u_out_pp = np.max(v_uout) - np.min(v_uout)
    print(f"Ausgangsspannung U_pp (uout, unskaliert): {u_out_pp:.3f} V")
    
    plt.figure(figsize=(width, width / 1.618))
    
    plt.plot(time, v_uout_scaled, label=r'$U_{\mathrm{out}} \times 150$', color='black', ls='-', lw=2)
    plt.plot(time, v_n001, label=r'$U_{\mathrm{IN+}}$', color='black', ls='--', alpha=0.8)
    plt.plot(time, v_n010, label=r'$U_{\mathrm{IN-}}$', color='black', ls=':', alpha=0.8)
    
    plt.xlabel(r'$t$ in ns')
    plt.ylabel(r'$U$ in V')
    plt.grid(True, alpha=0.6, color='gray', ls=':')
    
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().yaxis.set_major_formatter(formatter)
    
    plt.legend(loc='best', frameon=True, edgecolor="black") 
    plt.tight_layout()
    
    plt.savefig('bilder/plot_transient.pdf', format="pdf", bbox_inches="tight")
    print("Bild gespeichert unter: bilder/plot_transient.pdf")
    plt.show()

# ==========================================
# 2. AC-ANALYSE / BODE PLOT (.ac) GETEILT
# ==========================================
elif is_ac:
    print("\n=> AC-Analyse (.ac) erkannt!")
    
    frequency = ltr.get_trace('frequency').get_wave()
    v_uout = ltr.get_trace('V(uout)').get_wave()
    
    mask = frequency <= 250e6
    frequency = frequency[mask]
    v_uout = v_uout[mask]
    
    gain_db = 20 * np.log10(np.abs(v_uout))
    phase_deg = np.unwrap(np.angle(v_uout)) * (180 / np.pi) 
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(width, width), sharex=True)
    
    ax1.semilogx(frequency, gain_db, color='black', ls='-', lw=2)
    ax1.set_ylabel(r'Verstärkung in dB') 
    ax1.grid(True, which="both", color='gray', ls=":", alpha=0.6)
    ax1.yaxis.set_major_formatter(formatter)
    
    ax2.semilogx(frequency, phase_deg, color='black', ls='--', lw=2)
    ax2.set_xlabel(r'$f$ in Hz')
    ax2.set_ylabel(r'Phase $\varphi$ in $^\circ$')
    ax2.grid(True, which="both", color='gray', ls=":", alpha=0.6)
    ax2.yaxis.set_major_formatter(formatter)
    
    fig.tight_layout()
    plt.savefig('bilder/plot_bode_geteilt.pdf', format="pdf", bbox_inches="tight")
    print("Bild gespeichert unter: bilder/plot_bode_geteilt.pdf")
    plt.show()

# ==========================================
# 3. RAUSCH-ANALYSE (.noise)
# ==========================================
elif is_noise:
    print("\n=> Rausch-Analyse (.noise) erkannt!")
    
    frequency = ltr.get_trace('frequency').get_wave()
    
    if 'V(onoise)' in traces:
        onoise = ltr.get_trace('V(onoise)').get_wave()
    else:
        onoise = ltr.get_trace('onoise').get_wave()
    
    integrated_noise_sq = np.trapezoid(onoise**2, frequency)
    total_rms_noise = np.sqrt(integrated_noise_sq)
    
    print(f"Integriertes RMS-Rauschen: {total_rms_noise*1e6:.2f} µV")
    print(f"Erwartetes Peak-to-Peak Rauschen (Ausgang): {total_rms_noise * 6 * 1e3:.2f} mV")
    
    plt.figure(figsize=(width, width / 1.618))
    
    plt.loglog(frequency, onoise, color='black', ls='-', lw=2)
    plt.xlabel(r'$f$ in Hz')
    plt.ylabel(r'Rauschdichte in V/$\sqrt{\mathrm{Hz}}$')
    plt.grid(True, which="both", color='gray', ls=":", alpha=0.6)
    
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.tight_layout()
    
    plt.savefig('bilder/plot_noise.pdf', format="pdf", bbox_inches="tight")
    print("Bild gespeichert unter: bilder/plot_noise.pdf")
    plt.show()

else:
    print("\nFehler: Konnte den Simulationstyp nicht erkennen. Hast du eine .ac, .tran oder .noise Simulation laufen lassen?")