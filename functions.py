import openpyxl
from openpyxl.styles import PatternFill, Font
from tkinter import messagebox
from tasks import TodoTask, InProgressTask, DoneTask

# Stałe
NAZWA_PLIKU = "Tasks.xlsx"
KOLORY = {
    "Do zrobienia": "#FF9999",
    "W trakcie": "#FFFF99",
    "Wykonane": "#99FF99"
}

def sprawdz_lub_utworz_plik():
    try:
        skoroszyt = openpyxl.load_workbook(NAZWA_PLIKU)
    except FileNotFoundError:
        skoroszyt = openpyxl.Workbook()
        arkusz = skoroszyt.active
        arkusz.title = "Tasks"
        arkusz.append(["Title", "Status"])
        skoroszyt.save(NAZWA_PLIKU)
    return skoroszyt

def zaladuj_zadania():
    skoroszyt = sprawdz_lub_utworz_plik()
    arkusz = skoroszyt.active
    zadania = []
    for wiersz in arkusz.iter_rows(min_row=2, values_only=True):
        tytul, status = wiersz
        if status == "Do zrobienia":
            zadania.append(TodoTask(tytul))
        elif status == "W trakcie":
            zadania.append(InProgressTask(tytul))
        elif status == "Wykonane":
            zadania.append(DoneTask(tytul))
    return zadania

def zapisz_zadania(zadania):
    skoroszyt = openpyxl.Workbook()
    arkusz = skoroszyt.active
    arkusz.title = "Tasks"
    arkusz.append(["Title", "Status"])
    arkusz.column_dimensions['A'].width = 30
    arkusz.column_dimensions['B'].width = 15

    for zadanie in zadania:
        arkusz.append([zadanie.tytul, zadanie.status])
        wypelnienie = PatternFill(start_color=KOLORY[zadanie.status][1:],
                                end_color=KOLORY[zadanie.status][1:],
                                fill_type="solid")

        for komorka in arkusz.iter_rows(min_row=arkusz.max_row, max_row=arkusz.max_row, min_col=1, max_col=2):
            for k in komorka:
                k.fill = wypelnienie
                if zadanie.status == "W trakcie":
                    k.font = Font(bold=True)

    skoroszyt.save(NAZWA_PLIKU)

def dodaj_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    zadania.append(TodoTask(tytul))
    zapisz_zadania(zadania)
    if app_instance:
        app_instance.odswiez_liste_zadan()

def rozpocznij_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    for zadanie in zadania:
        if zadanie.tytul == tytul and zadanie.status == "Do zrobienia":
            zadanie.status = "W trakcie"
            zapisz_zadania(zadania)
            messagebox.showinfo("Sukces", f"Rozpoczęto zadanie: {tytul}")
            if app_instance:
                app_instance.odswiez_liste_zadan()
            return
    messagebox.showwarning("Ostrzeżenie", "Nie można rozpocząć tego zadania (nie istnieje lub ma niewłaściwy status)")

def zakoncz_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    for zadanie in zadania:
        if zadanie.tytul == tytul and zadanie.status == "W trakcie":
            zadanie.status = "Wykonane"
            zapisz_zadania(zadania)
            messagebox.showinfo("Sukces", f"Zakończono zadanie: {tytul}")
            if app_instance:
                app_instance.odswiez_liste_zadan()
            return
    messagebox.showwarning("Ostrzeżenie", "Nie można zakończyć tego zadania (nie istnieje lub ma niewłaściwy status)")