import tkinter as tk
from tkinter import ttk, messagebox, Menu
from functions import zaladuj_zadania, dodaj_zadanie, rozpocznij_zadanie, zakoncz_zadanie, usun_zadanie, KOLORY, \
    eksportuj_do_csv


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menedżer Zadań v0.9")
        self.root.geometry("750x550")

        self.setup_menu()
        self.setup_ui()
        self.odswiez_liste_zadan()

    def setup_menu(self):
        menubar = Menu(self.root)

        # Menu Plik
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Eksportuj do CSV", command=self.eksportuj_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjdź", command=self.root.quit)
        menubar.add_cascade(label="Plik", menu=file_menu)

        # Menu Pomoc (szkielet)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="O programie", command=self.show_about)
        menubar.add_cascade(label="Pomoc", menu=help_menu)

        self.root.config(menu=menubar)

    def setup_ui(self):
        # Główny kontener z zakładkami
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Zakładka wszystkie zadania
        tab_all = ttk.Frame(notebook)
        notebook.add(tab_all, text="Wszystkie zadania")

        # Panel dodawania zadań
        frame_dodaj = ttk.LabelFrame(tab_all, text="Dodaj nowe zadanie", padding=10)
        frame_dodaj.pack(fill=tk.X, padx=10, pady=5)

        self.entry_tytul = ttk.Entry(frame_dodaj)
        self.entry_tytul.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.btn_dodaj = ttk.Button(frame_dodaj, text="Dodaj", command=self.dodaj_zadanie_gui)
        self.btn_dodaj.pack(side=tk.LEFT)

        # Treeview z podwójnym kliknięciem
        frame_lista = ttk.LabelFrame(tab_all, text="Lista zadań", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_lista, columns=("tytul", "status", "data"), show="headings")
        self.tree.heading("tytul", text="Tytuł")
        self.tree.heading("status", text="Status")
        self.tree.heading("data", text="Data utworzenia")
        self.tree.column("tytul", width=300, anchor=tk.W)
        self.tree.column("status", width=120, anchor=tk.CENTER)
        self.tree.column("data", width=150, anchor=tk.CENTER)
        self.tree.bind("<Double-1>", self.edytuj_zadanie)

        vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_lista, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_lista.grid_rowconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(0, weight=1)

        # Panel akcji
        frame_akcje = ttk.Frame(tab_all, padding=10)
        frame_akcje.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_akcje, text="Rozpocznij", command=self.rozpocznij_zadanie_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_akcje, text="Zakończ", command=self.zakoncz_zadanie_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_akcje, text="Usuń", command=self.usun_zadanie_gui).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_akcje, text="Odśwież", command=self.odswiez_liste_zadan).pack(side=tk.RIGHT)

        # Zakładka statystyki (szkielet)
        tab_stats = ttk.Frame(notebook)
        notebook.add(tab_stats, text="Statystyki")
        ttk.Label(tab_stats, text="Statystyki będą dostępne w finalnej wersji").pack(pady=50)

    def show_about(self):
        messagebox.showinfo("O programie", "Menedżer Zadań v0.9\n(c) 2023")

    def edytuj_zadanie(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            messagebox.showinfo("Info", f"Edycja zadania '{item['values'][0]}'\nBędzie dostępna w finalnej wersji")

    def usun_zadanie_gui(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            tytul = item['values'][0]
            if messagebox.askyesno("Potwierdzenie", f"Czy na pewno usunąć zadanie: {tytul}?"):
                if usun_zadanie(tytul, self):
                    messagebox.showinfo("Sukces", f"Usunięto zadanie: {tytul}")
                else:
                    messagebox.showwarning("Błąd", "Nie udało się usunąć zadania")
        else:
            messagebox.showwarning("Ostrzeżenie", "Proszę wybrać zadanie z listy")

    def eksportuj_csv(self):
        try:
            eksportuj_do_csv()
            messagebox.showinfo("Sukces", "Dane wyeksportowane do pliku tasks_export.csv")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować danych: {str(e)}")

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
        for item in self.tree.get_children():
            self.tree.delete(item)

        zadania = zaladuj_zadania()
        for zadanie in zadania:
            item_id = self.tree.insert("", tk.END, values=(
                zadanie.tytul,
                zadanie.status,
                zadanie.data_utworzenia.strftime("%Y-%m-%d %H:%M")
            ))
            self.tree.tag_configure(item_id, background=KOLORY[zadanie.status])


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()


#TODO Pełna implementacja edycji zadań
#TODO Rozwinięte statystyki