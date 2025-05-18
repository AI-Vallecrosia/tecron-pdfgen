import tkinter as tk
from .main import main

def gui():
    # Crea la finestra principale
    root = tk.Tk()
    root.title("Generate Tecron PDF")

    # Aggiungi un'etichetta
    label = tk.Label(root, text="Ciao, mondo!")
    label.pack()

    # Aggiungi un pulsante
    def button_click():
        label.config(text="Generating PDF...")
        main()
        label.config(text="PDF Generated!")

    button = tk.Button(root, text="Click to generate PDF", command=button_click)
    button.pack()

    # Avvia l'applicazione
    root.mainloop()
