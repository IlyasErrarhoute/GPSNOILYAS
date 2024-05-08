# No GPS Mockup

## Einführung
Dieses Projekt präsentiert ein Mockup für ein System ohne GPS, das die Entfernungen und Winkel zwischen einem beweglichen Punkt M und den Eckpunkten eines Quadrats berechnet. Der bewegliche Punkt M kann auf dem Canvas verschoben werden, und die Entfernungen und Winkel werden in Echtzeit aktualisiert. Es gibt auch eine Option, um Linien und Kreise ein- oder auszublenden, um die Anzeige zu ändern. Die Berechnungen basieren auf der Regel von Pythagoras für die Entfernungen und der Regel von Tangens für die Winkel. Die Mitternachtsformel wird auch verwendet, um die Mitte des beweglichen Punktes zu finden.

## Code
Als graphische Benutzeroberfläche (GUI) wird Tkinter verwendet, da es einfach zu bedienen ist und eine große Community hat. Es werden auch mathematische Funktionen aus dem Modul "math" verwendet.

## Installation
- **Windows**: Stellen Sie sicher, dass Python installiert ist. Tkinter ist in den meisten Python-Installationen für Windows enthalten. Führen Sie die `main()` Funktion in der Datei `main.py` aus.
- **Linux**: Stellen Sie sicher, dass Python und Tkinter installiert sind. Sie können Tkinter mit dem folgenden Befehl installieren:
```bash
sudo apt-get install python3-tk
