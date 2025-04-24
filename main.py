import tkinter as tk
from tkinter import ttk, messagebox, Menu, simpledialog
from tkinter import font as tkfont
from functions import (
    zaladuj_zadania, dodaj_zadanie, edytuj_zadanie,
    rozpocznij_zadanie, zakoncz_zadanie, usun_zadanie,
    KOLORY, eksportuj_do_csv, generuj_statystyki
)
from datetime import datetime


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menedżer Zadań v1.0")
        self.root.geometry("850x600")
        self.root.minsize(700, 500)

        self.setup_fonts()
        self.setup_menu()
        self.setup_ui()
        self.odswiez_liste_zadan()

    def setup_fonts(self):
        self.custom_font = tkfont.Font(family="Segoe UI", size=10)
        self.bold_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")

    def setup_menu(self):
        menubar = Menu(self.root)

        # Menu Plik
        file_menu = Menu(menubar, tearoff=0, font=self.custom_font)
        file_menu.add_command(
            label="Eksportuj do CSV",
            command=self.eksportuj_csv,
            accelerator="Ctrl+E"
        )
        file_menu.add_separator()
        file_menu.add_command(
            label="Wyjdź",
            command=self.root.quit,
            accelerator="Ctrl+Q"
        )
        menubar.add_cascade(label="Plik", menu=file_menu)

        # Menu Zadania
        task_menu = Menu(menubar, tearoff=0, font=self.custom_font)
        task_menu.add_command(
            label="Dodaj zadanie",
            command=self.focus_add_entry,
            accelerator="Ctrl+N"
        )
        task_menu.add_command(
            label="Edytuj zadanie",
            command=self.edytuj_zadanie_gui,
            accelerator="Ctrl+D"
        )
        menubar.add_cascade(label="Zadania", menu=task_menu)

        # Menu Pomoc
        help_menu = Menu(menubar, tearoff=0, font=self.custom_font)
        help_menu.add_command(
            label="O programie",
            command=self.show_about
        )
        help_menu.add_command(
            label="Skróty klawiszowe",
            command=self.show_shortcuts
        )
        menubar.add_cascade(label="Pomoc", menu=help_menu)

        self.root.config(menu=menubar)

        # Skróty klawiszowe
        self.root.bind("<Control-e>", lambda e: self.eksportuj_csv())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        self.root.bind("<Control-n>", lambda e: self.focus_add_entry())
        self.root.bind("<Control-d>", lambda e: self.edytuj_zadanie_gui())

    def setup_ui(self):
        # Główny kontener z zakładkami
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Zakładka wszystkie zadania
        tab_all = ttk.Frame(self.notebook)
        self.notebook.add(tab_all, text="Wszystkie zadania")

        # Panel dodawania zadań
        frame_dodaj = ttk.LabelFrame(
            tab_all,
            text=" Dodaj nowe zadanie ",
            padding=10
        )
        frame_dodaj.pack(fill=tk.X, padx=10, pady=5)

        self.entry_tytul = ttk.Entry(
            frame_dodaj,
            font=self.custom_font
        )
        self.entry_tytul.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.entry_tytul.bind("<Return>", lambda e: self.dodaj_zadanie_gui())

        self.btn_dodaj = ttk.Button(
            frame_dodaj,
            text="Dodaj",
            command=self.dodaj_zadanie_gui
        )
        self.btn_dodaj.pack(side=tk.LEFT)

        # Treeview
        frame_lista = ttk.LabelFrame(
            tab_all,
            text=" Lista zadań ",
            padding=10
        )
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(
            frame_lista,
            columns=("tytul", "status", "data", "deadline"),
            show="headings",
            selectmode="browse"
        )

        # Konfiguracja kolumn
        columns = [
            ("tytul", "Tytuł", 300, tk.W),
            ("status", "Status", 120, tk.CENTER),
            ("data", "Data utworzenia", 150, tk.CENTER),
            ("deadline", "Termin", 150, tk.CENTER)
        ]

        for col_id, text, width, anchor in columns:
            self.tree.heading(col_id, text=text)
            self.tree.column(col_id, width=width, anchor=anchor)

        # Scrollbary
        vsb = ttk.Scrollbar(
            frame_lista,
            orient="vertical",
            command=self.tree.yview
        )
        hsb = ttk.Scrollbar(
            frame_lista,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        frame_lista.grid_rowconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(0, weight=1)

        # Panel akcji
        frame_akcje = ttk.Frame(tab_all, padding=10)
        frame_akcje.pack(fill=tk.X, padx=10, pady=5)

        actions = [
            ("Rozpocznij", self.rozpocznij_zadanie_gui),
            ("Zakończ", self.zakoncz_zadanie_gui),
            ("Edytuj", self.edytuj_zadanie_gui),
            ("Usuń", self.usun_zadanie_gui),
            ("Odśwież", self.odswiez_liste_zadan)
        ]

        for text, command in actions[:3]:
            ttk.Button(
                frame_akcje,
                text=text,
                command=command
            ).pack(side=tk.LEFT, padx=5)

        ttk.Frame(frame_akcje, width=20).pack(side=tk.LEFT)  # separator

        for text, command in actions[3:]:
            ttk.Button(
                frame_akcje,
                text=text,
                command=command
            ).pack(side=tk.LEFT, padx=5)

        # Zakładka statystyki
        self.tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stats, text="Statystyki")
        self.setup_stats_tab()

    def setup_stats_tab(self):
        # Ramka na statystyki
        stats_frame = ttk.LabelFrame(
            self.tab_stats,
            text=" Podsumowanie ",
            padding=15
        )
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Etykiety statystyk
        self.stats_labels = {}
        stats = [
            ("Wszystkie zadania", "total"),
            ("Do zrobienia", "todo"),
            ("W trakcie", "in_progress"),
            ("Wykonane", "done"),
            ("Zaległe", "overdue")
        ]

        for i, (text, key) in enumerate(stats):
            frame = ttk.Frame(stats_frame)
            frame.grid(row=i, column=0, sticky="w", pady=3)

            ttk.Label(
                frame,
                text=f"{text}:",
                font=self.bold_font,
                width=15
            ).pack(side=tk.LEFT)

            self.stats_labels[key] = ttk.Label(
                frame,
                text="0",
                font=self.custom_font
            )
            self.stats_labels[key].pack(side=tk.LEFT)

        # Przycisk odświeżania statystyk
        ttk.Button(
            stats_frame,
            text="Odśwież statystyki",
            command=self.odswiez_statystyki
        ).grid(row=len(stats), column=0, pady=10)

    def odswiez_statystyki(self):
        stats = generuj_statystyki()
        for key, value in stats.items():
            self.stats_labels[key].config(text=value)

    def focus_add_entry(self):
        self.notebook.select(0)  # Przełącz na pierwszą zakładkę
        self.entry_tytul.focus_set()

    def show_about(self):
        about_text = (
            "Menedżer Zadań v1.0\n\n"
            "Aplikacja do zarządzania zadaniami\n"
            "z podziałem na statusy:\n"
            "- Do zrobienia\n"
            "- W trakcie\n"
            "- Wykonane\n\n"
            "© 2023 - Finalna wersja"
        )
        messagebox.showinfo("O programie", about_text)

    def show_shortcuts(self):
        shortcuts = (
            "Skróty klawiszowe:\n\n"
            "Ctrl+N - Dodaj nowe zadanie\n"
            "Ctrl+D - Edytuj zadanie\n"
            "Ctrl+E - Eksport do CSV\n"
            "Ctrl+Q - Wyjście z programu\n\n"
            "Enter - Potwierdź dodawanie zadania"
        )
        messagebox.showinfo("Skróty klawiszowe", shortcuts)

    def get_selected_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ostrzeżenie", "Proszę wybrać zadanie z listy")
            return None
        return self.tree.item(selected_item[0])

    def edytuj_zadanie_gui(self, event=None):
        item = self.get_selected_task()
        if not item:
            return

        tytul = item['values'][0]
        nowy_tytul = simpledialog.askstring(
            "Edytuj zadanie",
            "Wprowadź nowy tytuł:",
            initialvalue=tytul,
            parent=self.root
        )

        if nowy_tytul and nowy_tytul != tytul:
            if edytuj_zadanie(tytul, nowy_tytul, self):
                messagebox.showinfo("Sukces", "Zaktualizowano zadanie")
            else:
                messagebox.showwarning("Błąd", "Nie udało się zaktualizować zadania")

    def usun_zadanie_gui(self):
        item = self.get_selected_task()
        if not item:
            return

        tytul = item['values'][0]
        if messagebox.askyesno(
                "Potwierdzenie",
                f"Czy na pewno usunąć zadanie:\n\n{tytul}?",
                icon="warning"
        ):
            if usun_zadanie(tytul, self):
                messagebox.showinfo("Sukces", f"Usunięto zadanie: {tytul}")
            else:
                messagebox.showwarning("Błąd", "Nie udało się usunąć zadania")

    def eksportuj_csv(self, event=None):
        try:
            eksportuj_do_csv()
            messagebox.showinfo(
                "Sukces",
                "Dane wyeksportowane do pliku:\n\ntasks_export.csv"
            )
        except Exception as e:
            messagebox.showerror(
                "Błąd",
                f"Nie udało się wyeksportować danych:\n\n{str(e)}"
            )

    def dodaj_zadanie_gui(self, event=None):
        tytul = self.entry_tytul.get().strip()
        if not tytul:
            messagebox.showwarning(
                "Ostrzeżenie",
                "Proszę wprowadzić tytuł zadania"
            )
            return

        deadline = self.ask_for_deadline()
        if deadline is False:  # Anulowano
            return

        if dodaj_zadanie(tytul, deadline, self):
            self.entry_tytul.delete(0, tk.END)
        else:
            messagebox.showwarning(
                "Ostrzeżenie",
                "Nie udało się dodać zadania"
            )

    def ask_for_deadline(self):
        result = messagebox.askyesno(
            "Termin wykonania",
            "Czy chcesz ustawić termin wykonania zadania?"
        )

        if not result:
            return None

        while True:
            date_str = simpledialog.askstring(
                "Termin wykonania",
                "Podaj termin (YYYY-MM-DD):",
                parent=self.root
            )

            if not date_str:  # Anulowano
                return False

            try:
                deadline = datetime.strptime(date_str, "%Y-%m-%d").date()
                return deadline.strftime("%Y-%m-%d")
            except ValueError:
                messagebox.showerror(
                    "Błąd",
                    "Nieprawidłowy format daty. Wprowadź datę w formacie RRRR-MM-DD"
                )

    def rozpocznij_zadanie_gui(self):
        item = self.get_selected_task()
        if not item:
            return

        tytul = item['values'][0]
        if rozpocznij_zadanie(tytul, self):
            messagebox.showinfo(
                "Sukces",
                f"Rozpoczęto zadanie: {tytul}"
            )

    def zakoncz_zadanie_gui(self):
        item = self.get_selected_task()
        if not item:
            return

        tytul = item['values'][0]
        if zakoncz_zadanie(tytul, self):
            messagebox.showinfo(
                "Sukces",
                f"Zakończono zadanie: {tytul}"
            )

    def odswiez_liste_zadan(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        zadania = zaladuj_zadania()
        today = datetime.now().date()

        for zadanie in zadania:
            deadline = zadanie.deadline
            overdue = False

            if deadline:
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                    overdue = deadline_date < today
                except ValueError:
                    pass

            values = (
                zadanie.tytul,
                zadanie.status,
                zadanie.data_utworzenia.strftime("%Y-%m-%d %H:%M"),
                zadanie.deadline if zadanie.deadline else "Brak"
            )

            item_id = self.tree.insert("", tk.END, values=values)

            # Kolorowanie wierszy
            tags = []
            if zadanie.status == "W trakcie":
                tags.append("in_progress")
            elif zadanie.status == "Wykonane":
                tags.append("done")
            else:
                tags.append("todo")

            if overdue and zadanie.status != "Wykonane":
                tags.append("overdue")

            self.tree.item(item_id, tags=tags)

        # Konfiguracja tagów dla kolorów
        self.tree.tag_configure("todo", background=KOLORY["Do zrobienia"])
        self.tree.tag_configure("in_progress", background=KOLORY["W trakcie"])
        self.tree.tag_configure("done", background=KOLORY["Wykonane"])
        self.tree.tag_configure("overdue", foreground="#FF0000")

        # Odśwież statystyki
        self.odswiez_statystyki()


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()