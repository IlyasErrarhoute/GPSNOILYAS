
import tkinter as tk
import math
class NoGpsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NO GPS Mockup") 
        self.root.resizable(True, True)

        # Canvas Panel wird erstellt, um das Quadrat, die Punkte, Linien und Kreise zu zeichnen.
        self.canvas = tk.Canvas(root , bg="mint cream", width=600, height=600)
        self.canvas.pack(side="left", padx=50, pady=50 , fill="both", expand=False )

        # Quadrat und Punkte zeichnen
        self.quadrat_zeichnen()

        # Unsere Beweglicher Punkt M erstellen
        self.beweglicher_punkt = self.canvas.create_oval(292.5, 292.5, 307.5, 307.5, fill="red", tags="beweglich")
        #tag_bind() Methode wird verwendet, um eine Funktion aufzurufen, wenn ein bestimmtes Ereignis auftritt.
        self.canvas.tag_bind("beweglich", "<B1-Motion>", self.punkt_bewegen)
        
        # Erstellung von Linien von die von M zu A, B, C, D gehen und sich aktualisieren lassen falls sich der Punkt bewegt
        self.linien = {}
        self.linien_aktualisieren()
        # Erausstellung von Kreisen um die Punkte A, B, C, D mit Radien entsprechend der Entfernungen von M und sich aktualisieren lassen falls sich der Punkt bewegt                                                       
        self.kreise = {}
        self.kreise_aktualisieren()
        
        # Distanztabelle erstellen , diese wird sich aktualisieren lassen falls sich der Punkt bewegt
        self.distanz_tabelle = tk.LabelFrame(root, text="Distanzen", bg="#1E1E1E", fg="white", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        self.distanz_tabelle.pack(side="top", padx=10, pady=10, anchor="ne", fill="x")
        self.distanz_labels = {}
        self.distanzen_aktualisieren()
        
        # Winkel Tabelle erstellen , diese wird sich aktualisieren lassen falls sich der Punkt bewegt
        self.winkel_tabelle = tk.LabelFrame(root, text="Winkel", bg="#1E1E1E", fg="white", padx=10, pady=10, font=("Helvetica", 12, "bold"))
        self.winkel_tabelle.pack(side="top", padx=10, pady=10, anchor="ne", fill="x")
        self.winkel_labels = {}
        self.winkel_aktualisieren()
        
        # "Anzeige" Button erstellen , dieser wird ein Popup-Fenster öffnen wenn er gedrückt wird , um Optionen zu ändern wie Linien und Kreise ein/ausblenden
        self.anzeige_button = tk.Button(root, text="Anzeige", command=self.popup_öffnen, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        self.anzeige_button.pack(side="top", pady=5)
    
    # Funktionen die in der Klasse NoGpsApp definiert sind 


    def quadrat_zeichnen(self):
        # Koordinaten der Punkte A, B, C, D definieren auf dem Canvas
        self.punkte = {
            "A": (150, 150),
            "B": (450, 150),
            "C": (450, 450),
            "D": (150, 450)
        }
        
        # Linien zwischen den Punkten zeichnen, um ein Quadrat Ebene zu erstellen
        self.canvas.create_line(self.punkte["A"], self.punkte["B"], width=13, tags="AB")
        self.canvas.create_line(self.punkte["B"], self.punkte["C"], width=13, tags="BC")
        self.canvas.create_line(self.punkte["C"], self.punkte["D"], width=13, tags="CD")
        self.canvas.create_line(self.punkte["D"], self.punkte["A"], width=13, tags="DA")
        
        # Punkte A, B, C, D markieren
        for punkt, koordinaten in self.punkte.items():
            self.canvas.create_oval(koordinaten[0]-7, koordinaten[1]-7, koordinaten[0]+7, koordinaten[1]+7, fill="black")
            if punkt in ['C', 'D']:
                self.canvas.create_text(koordinaten[0], koordinaten[1]+15, text=punkt, anchor="center", fill="black")
            else:
                self.canvas.create_text(koordinaten[0], koordinaten[1]-15, text=punkt, anchor="center", fill="black")
    
    def punkt_bewegen(self, event):
        # Beweglichen Punkt M bewegen
        # Ich war unsicher ob Sie wollen dass der Punkt M sich nur innerhalb des Quadrats bewegen kann oder überall auf dem Canvas
        # Ich bin davon Ausgegangen dass der Punkt M eine Abstraktes Punkte ist und kann sich überall auf dem Canvas bewegen

        x, y = event.x, event.y # x und y Koordinaten des Mauszeigers

        if 50 <= x <= 550 and 50 <= y <= 550: # Ein Einschränkung für die Bewegung des Punktes M war aber hier Notwendig so dass Platz für die Statistiken und Anzeigeoptionen bleibt

            self.canvas.coords(self.beweglicher_punkt, x-7.5, y-7.5, x+7.5, y+7.5)
            self.linien_aktualisieren()
            self.kreise_aktualisieren()
            self.distanzen_aktualisieren()
            self.winkel_aktualisieren()
    
    def linien_aktualisieren(self):
        # Linien von M zu A, B, C, D aktualisieren , wenn sich der Punkt M bewegt
        beweglicher_koordinaten = self.canvas.coords(self.beweglicher_punkt)
        #hier wird die Regel von Mitternachtsformel angewendet um die Mitte des Punktes zu finden
        M = ((beweglicher_koordinaten[0] + beweglicher_koordinaten[2]) / 2, (beweglicher_koordinaten[1] + beweglicher_koordinaten[3]) / 2)
        
        for punkt, koordinaten in self.punkte.items():
            # M[0] und M[1] sind die Koordinaten des Mittelpunktes des beweglichen Punktes M
            if punkt in self.linien:
                self.canvas.coords(self.linien[punkt], M[0], M[1], koordinaten[0]+5.5, koordinaten[1]+5.5)
            else:
                self.linien[punkt] = self.canvas.create_line(M[0], M[1], koordinaten[0], koordinaten[1], fill="blue")
    
    def kreise_aktualisieren(self):
        # Kreise um Punkte A, B, C, D mit Radien entsprechend der Entfernungen von M aktualisieren
        beweglicher_koordinaten = self.canvas.coords(self.beweglicher_punkt)
        M = ((beweglicher_koordinaten[0] + beweglicher_koordinaten[2]) / 2, (beweglicher_koordinaten[1] + beweglicher_koordinaten[3]) / 2)
        
        for punkt, koordinaten in self.punkte.items():
            # Hier wird die Regel von Pythagoras angewendet um die Distanz zwischen zwei Punkten zu berechnen
            distanz = math.sqrt((M[0] - koordinaten[0]) ** 2 + (M[1] - koordinaten[1]) ** 2)
            if punkt in self.kreise:
                
                self.canvas.coords(self.kreise[punkt], koordinaten[0]-distanz, koordinaten[1]-distanz, koordinaten[0]+distanz, koordinaten[1]+distanz)
            else:
                self.kreise[punkt] = self.canvas.create_oval(koordinaten[0]-distanz, koordinaten[1]-distanz, koordinaten[0]+distanz, koordinaten[1]+distanz, outline="blue")
  
    
    def distanzen_aktualisieren(self):
        # Distanzen von M zu A, B, C, D berechnen und die Tabelle aktualisieren 
        # hier wird auch die Regel von Pythagoras und die Regel von Mitternachtsformel angewendet
        
        beweglicher_koordinaten = self.canvas.coords(self.beweglicher_punkt)
        M = ((beweglicher_koordinaten[0] + beweglicher_koordinaten[2]) / 2, (beweglicher_koordinaten[1] + beweglicher_koordinaten[3]) / 2)
        schwelle = 10
        for punkt, koordinaten in self.punkte.items():
            distanz = math.sqrt((M[0] - koordinaten[0]) ** 2 + (M[1] - koordinaten[1]) ** 2)
            if distanz < schwelle:
                distanz = 0
            if punkt in self.distanz_labels:
                self.distanz_labels[punkt].config(text=f"{punkt}M: {distanz:.2f}")
            else:
                self.distanz_labels[punkt] = tk.Label(self.distanz_tabelle, text=f"{punkt}M: {distanz:.2f}", bg="#1E1E1E", fg="white", font=("Helvetica", 10))
                self.distanz_labels[punkt].pack(fill="x")
    
    # die Brechnung ist mit Pixeln 
    #  die menschliche Augen können nicht die Unterschiede zwischen 0.0264583333 cm  und 0.0529166667 cm gut merken
    # Deshalb habe ich ein Schwellenwert von 10 Pixeln festgelegt 
    # Jetzt sind die Ergebnisse näher an der menschlichen Wahrnehmung und die Winkel werden richtig aktualisiert
    def winkel_aktualisieren(self):
        # Koodinaten von Punkten A, M, B, C, D
        A_koordinaten = self.punkte["A"]
        M_koordinaten = self.canvas.coords(self.beweglicher_punkt)
        B_koordinaten = self.punkte["B"]
        C_koordinaten = self.punkte["C"]
        D_koordinaten = self.punkte["D"]
        
        # Schwellenwert für das Betrachten von Punkten als koinzident
        schwellenwert = 10
        
        # Distanzen berechnen mit der Regel von Pythagoras
        AM = math.sqrt((M_koordinaten[0] - A_koordinaten[0]) ** 2 + (M_koordinaten[1] - A_koordinaten[1]) ** 2)
        MB = math.sqrt((B_koordinaten[0] - M_koordinaten[2]) ** 2 + (B_koordinaten[1] - M_koordinaten[3]) ** 2)
        MC = math.sqrt((C_koordinaten[0] - M_koordinaten[2]) ** 2 + (C_koordinaten[1] - M_koordinaten[3]) ** 2)
        MD = math.sqrt((D_koordinaten[0] - M_koordinaten[2]) ** 2 + (D_koordinaten[1] - M_koordinaten[3]) ** 2)
        
        # Winkel in Bogenmaß berechnen mit der Regel von Tangens
       
        winkel_AMB = math.atan2(B_koordinaten[1] - M_koordinaten[1], B_koordinaten[0] - M_koordinaten[0]) - math.atan2(A_koordinaten[1] - M_koordinaten[1], A_koordinaten[0] - M_koordinaten[0])
        winkel_BMC = math.atan2(C_koordinaten[1] - M_koordinaten[1], C_koordinaten[0] - M_koordinaten[0]) - math.atan2(B_koordinaten[1] - M_koordinaten[1], B_koordinaten[0] - M_koordinaten[0])
        winkel_CMD = math.atan2(D_koordinaten[1] - M_koordinaten[1], D_koordinaten[0] - M_koordinaten[0]) - math.atan2(C_koordinaten[1] - M_koordinaten[1], C_koordinaten[0] - M_koordinaten[0])
        winkel_DMA = math.atan2(A_koordinaten[1] - M_koordinaten[1], A_koordinaten[0] - M_koordinaten[0]) - math.atan2(D_koordinaten[1] - M_koordinaten[1], D_koordinaten[0] - M_koordinaten[0])
        
        # Winkel in Grad umwandeln
        winkel_AMB = math.degrees(winkel_AMB) % 360 
        winkel_BMC = math.degrees(winkel_BMC) % 360
        winkel_CMD = math.degrees(winkel_CMD) % 360
        winkel_DMA = math.degrees(winkel_DMA) % 360

        
        
        
        # Winkel korrigieren, wenn M mit einem der Eckpunkte koinzidiert
        if AM < schwellenwert or MB < schwellenwert:
            winkel_AMB = 0
        if MB < schwellenwert or MC < schwellenwert:
            winkel_BMC = 0
        if MC < schwellenwert or MD < schwellenwert:
            winkel_CMD = 0
        if MD < schwellenwert or AM < schwellenwert:
            winkel_DMA = 0
        
        
        
        # Tabelle mit den Winkeln aktualisieren
        if "AMB" in self.winkel_labels:
            self.winkel_labels["AMB"].config(text=f"Winkel AMB: {winkel_AMB:.2f}°")
        else:
            self.winkel_labels["AMB"] = tk.Label(self.winkel_tabelle, text=f"Winkel AMB: {winkel_AMB:.2f}°", bg="#1E1E1E", fg="white", font=("Helvetica", 10))
            self.winkel_labels["AMB"].pack(fill="x")
        
        if "BMC" in self.winkel_labels:
            self.winkel_labels["BMC"].config(text=f"Winkel BMC: {winkel_BMC:.2f}°")
        else:
            self.winkel_labels["BMC"] = tk.Label(self.winkel_tabelle, text=f"Winkel BMC: {winkel_BMC:.2f}°", bg="#1E1E1E", fg="white", font=("Helvetica", 10))
            self.winkel_labels["BMC"].pack(fill="x")
        
        if "CMD" in self.winkel_labels:
            self.winkel_labels["CMD"].config(text=f"Winkel CMD: {winkel_CMD:.2f}°")
        else:
            self.winkel_labels["CMD"] = tk.Label(self.winkel_tabelle, text=f"Winkel CMD: {winkel_CMD:.2f}°", bg="#1E1E1E", fg="white", font=("Helvetica", 10))
            self.winkel_labels["CMD"].pack(fill="x")
        
        if "DMA" in self.winkel_labels:
            self.winkel_labels["DMA"].config(text=f"Winkel DMA: {winkel_DMA:.2f}°")
        else:
            self.winkel_labels["DMA"] = tk.Label(self.winkel_tabelle, text=f"Winkel DMA: {winkel_DMA:.2f}°", bg="#1E1E1E", fg="white", font=("Helvetica", 10))
            self.winkel_labels["DMA"].pack(fill="x")
   
    # Popup-Fenster öffnen, um Optionen zu ändern wie Linien und Kreise ein/ausblenden
    def popup_öffnen(self):
        popup = tk.Toplevel(self.root)
        popup.title("Optionen")
        
        kreise_ein_aus_button = tk.Button(popup, text="Kreise Ein/Ausblenden", command=self.kreise_ein_aus, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        kreise_ein_aus_button.pack(pady=5)
        
        linien_ein_aus_button = tk.Button(popup, text="Linien Ein/Ausblenden", command=self.linien_ein_aus, bg="#007ACC", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        linien_ein_aus_button.pack(pady=5)

    def kreise_ein_aus(self):
        if self.kreise:
            for kreis in self.kreise.values():
                zustand = self.canvas.itemcget(kreis, "state")   
                if zustand == "normal" or zustand == "":
                    neuer_zustand = "hidden"
                else:
                    neuer_zustand = "normal"
                self.canvas.itemconfigure(kreis, state=neuer_zustand)
    
    def linien_ein_aus(self):
        if self.linien:
            for linie in self.linien.values():
                zustand = self.canvas.itemcget(linie, "state")
                if zustand == "normal" or zustand == "":
                    neuer_zustand = "hidden"
                else:
                    neuer_zustand = "normal"
                self.canvas.itemconfigure(linie, state=neuer_zustand)

def main():
    root = tk.Tk()
    app = NoGpsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


