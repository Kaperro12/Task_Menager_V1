import tkinter as tk
from tkinter import ttk, messagebox
from functions import zaladuj_zadania, dodaj_zadanie

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menedżer Zadań v0.2")
        self.root.geometry("500x400")

        self.setup_basic_ui()
        self.odswiez_liste_zadan()

    def setup_basic_ui(self):
        # Ramka dla formularza dodawania zadania
        frame_dodaj = ttk.LabelFrame(self.root, text="Dodaj nowe zadanie", padding=10)
        frame_dodaj.pack(fill=tk.X, padx=10, pady=5)

        self.entry_tytul = ttk.Entry(frame_dodaj)
        self.entry_tytul.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        btn_dodaj = ttk.Button(frame_dodaj, text="Dodaj", command=self.dodaj_zadanie_gui)
        btn_dodaj.pack(side=tk.LEFT)

        # Ramka dla listy zadań
        frame_lista = ttk.LabelFrame(self.root, text="Lista zadań", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Prosta lista zamiast Treeview (do wymiany w przyszłości)
        self.lista_zadan = tk.Listbox(frame_lista)
        self.lista_zadan.pack(fill=tk.BOTH, expand=True)

        # TODO: Dodać przyciski akcji (rozpocznij/zakończ)
        # TODO: Zastąpić Listbox Treeview z kolumnami

    def dodaj_zadanie_gui(self):
        tytul = self.entry_tytul.get().strip()
        if tytul:
            dodaj_zadanie(tytul)
            self.entry_tytul.delete(0, tk.END)
            self.odswiez_liste_zadan()
        else:
            messagebox.showwarning("Ostrzeżenie", "Proszę wprowadzić tytuł zadania")

    def odswiez_liste_zadan(self):
        self.lista_zadan.delete(0, tk.END)
        zadania = zaladuj_zadania()
        for zadanie in zadania:
            self.lista_zadan.insert(tk.END, f"{zadanie.tytul} ({zadanie.status})")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()