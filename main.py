import tkinter as tk
from tkinter import ttk, messagebox
from functions import zaladuj_zadania, dodaj_zadanie, rozpocznij_zadanie, zakoncz_zadanie, KOLORY

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menedżer Zadań v0.3")
        self.root.geometry("600x450")

        self.setup_ui()
        self.odswiez_liste_zadan()

    def setup_ui(self):
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

        # Treeview do wyświetlania zadań
        self.tree = ttk.Treeview(frame_lista, columns=("tytul", "status"), show="headings")
        self.tree.heading("tytul", text="Tytuł")
        self.tree.heading("status", text="Status")
        self.tree.column("tytul", width=350, anchor=tk.W)
        self.tree.column("status", width=150, anchor=tk.CENTER)

        vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_lista, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_lista.grid_rowconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(0, weight=1)

        # Ramka dla przycisków akcji
        frame_akcje = ttk.Frame(self.root, padding=10)
        frame_akcje.pack(fill=tk.X, padx=10, pady=5)

        btn_rozpocznij = ttk.Button(frame_akcje, text="Rozpocznij", command=self.rozpocznij_zadanie_gui)
        btn_rozpocznij.pack(side=tk.LEFT, padx=5)

        btn_zakoncz = ttk.Button(frame_akcje, text="Zakończ", command=self.zakoncz_zadanie_gui)
        btn_zakoncz.pack(side=tk.LEFT, padx=5)

        btn_odswiez = ttk.Button(frame_akcje, text="Odśwież", command=self.odswiez_liste_zadan)
        btn_odswiez.pack(side=tk.RIGHT)

    def dodaj_zadanie_gui(self):
        tytul = self.entry_tytul.get().strip()
        if tytul:
            dodaj_zadanie(tytul, self)
            self.entry_tytul.delete(0, tk.END)
        else:
            messagebox.showwarning("Ostrzeżenie", "Proszę wprowadzić tytuł zadania")

    def rozpocznij_zadanie_gui(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            tytul = item['values'][0]
            rozpocznij_zadanie(tytul, self)
        else:
            messagebox.showwarning("Ostrzeżenie", "Proszę wybrać zadanie z listy")

    def zakoncz_zadanie_gui(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            tytul = item['values'][0]
            zakoncz_zadanie(tytul, self)
        else:
            messagebox.showwarning("Ostrzeżenie", "Proszę wybrać zadanie z listy")

    def odswiez_liste_zadan(self):
        # Usuń wszystkie elementy z Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Załaduj i wyświetl zadania
        zadania = zaladuj_zadania()
        for zadanie in zadania:
            item_id = self.tree.insert("", tk.END, values=(zadanie.tytul, zadanie.status))
            self.tree.tag_configure(item_id, background=KOLORY[zadanie.status])

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()