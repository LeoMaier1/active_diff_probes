# Projektdaten Bachelorarbeit

Dieses Repository enthält alle Projekt-, Hardware- und Simulationsdaten, die im Rahmen meiner Bachelorarbeit erstellt wurden.

## Ordnerstruktur

* **`01_Simulation/`**
  * `ltspice/`: Beinhaltet die nativen LTspice-Simulationsdateien.
  * `pyltspice/`: Enthält die Python-Skripte zur automatisierten Auswertung der Simulationsergebnisse.
* **`02_3D_Modelle/`**
  * `inventor/`: Native Autodesk Inventor Baugruppen (`.iam`) und Bauteile (`.ipt`) inkl. Projektdatei.
  * `*.step`: Exportierte 3D-Modelle der einzelnen Gehäuse für den schnellen Import in andere CAD-Systeme.
* **`03_Hardware/`**
  * Native Altium Designer Projektdateien (Schaltpläne und Layouts).
  * `Produktionsdaten/`: Exportierte Schaltpläne als PDF zur Dokumentation.
    * `Produktionsfiles_aisler/`: Vollständige Fertigungsdaten (Camtastic, Gerber, Bohrdaten), aufbereitet für die Fertigung bei Aisler.
* **`requirements.txt`**: Auflistung der benötigten Python-Bibliotheken.

## Python Setup (Simulationen)
Um die Python-Auswertungsskripte im Ordner `01_Simulation/pyltspice/` lokal auszuführen, installieren Sie bitte vorab die benötigten Bibliotheken:
```bash
pip install -r requirements.txt
