import openpyxl
import csv
from openpyxl.styles import PatternFill, Font
from tkinter import messagebox
from datetime import datetime
from tasks import TodoTask, InProgressTask, DoneTask

NAZWA_PLIKU = "Tasks.xlsx"
KOLORY = {
    "Do zrobienia": "#FF9999",
    "W trakcie": "#FFFF99",
    "Wykonane": "#99FF99"
}


def sprawdz_lub_utworz_plik():
    try:
        return openpyxl.load_workbook(NAZWA_PLIKU)
    except FileNotFoundError:
        skoroszyt = openpyxl.Workbook()
        arkusz = skoroszyt.active
        arkusz.title = "Tasks"
        arkusz.append(["Title", "Status", "CreationDate"])
        skoroszyt.save(NAZWA_PLIKU)
        return skoroszyt


def zaladuj_zadania():
    skoroszyt = sprawdz_lub_utworz_plik()
    arkusz = skoroszyt.active
    zadania = []

    for wiersz in arkusz.iter_rows(min_row=2, values_only=True):
        if len(wiersz) == 0:
            continue

        tytul = wiersz[0]
        status = wiersz[1] if len(wiersz) > 1 else "Do zrobienia"
        data = datetime.strptime(wiersz[2], "%Y-%m-%d %H:%M:%S") if len(wiersz) > 2 else datetime.now()

        if status == "Do zrobienia":
            zadanie = TodoTask(tytul)
        elif status == "W trakcie":
            zadanie = InProgressTask(tytul)
        elif status == "Wykonane":
            zadanie = DoneTask(tytul)
        else:
            zadanie = TodoTask(tytul)

        zadanie.data_utworzenia = data
        zadania.append(zadanie)

    return zadania


def zapisz_zadania(zadania):
    skoroszyt = openpyxl.Workbook()
    arkusz = skoroszyt.active
    arkusz.title = "Tasks"
    arkusz.append(["Title", "Status", "CreationDate"])

    arkusz.column_dimensions['A'].width = 40
    arkusz.column_dimensions['B'].width = 15
    arkusz.column_dimensions['C'].width = 20

    for zadanie in zadania:
        arkusz.append([
            zadanie.tytul,
            zadanie.status,
            zadanie.data_utworzenia.strftime("%Y-%m-%d %H:%M:%S")
        ])

        wypelnienie = PatternFill(
            start_color=KOLORY[zadanie.status][1:],
            end_color=KOLORY[zadanie.status][1:],
            fill_type="solid"
        )

        for komorka in arkusz.iter_rows(min_row=arkusz.max_row, max_row=arkusz.max_row, min_col=1, max_col=3):
            for k in komorka:
                k.fill = wypelnienie
                if zadanie.status == "W trakcie":
                    k.font = Font(bold=True)

    skoroszyt.save(NAZWA_PLIKU)


def eksportuj_do_csv():
    zadania = zaladuj_zadania()
    with open('tasks_export.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tytuł', 'Status', 'Data utworzenia', 'Data eksportu'])
        for zadanie in zadania:
            writer.writerow([
                zadanie.tytul,
                zadanie.status,
                zadanie.data_utworzenia.strftime("%Y-%m-%d %H:%M"),
                datetime.now().strftime("%Y-%m-%d %H:%M")
            ])


def dodaj_zadanie(tytul, app_instance=None):
    if not tytul or len(tytul.strip()) == 0:
        messagebox.showwarning("Ostrzeżenie", "Tytuł zadania nie może być pusty")
        return False

    if len(tytul) > 100:
        messagebox.showwarning("Ostrzeżenie", "Tytuł zadania jest zbyt długi (max 100 znaków)")
        return False

    zadania = zaladuj_zadania()

    # Prosta walidacja duplikatów
    if any(z.tytul.lower() == tytul.lower() for z in zadania):
        messagebox.showwarning("Ostrzeżenie", "Zadanie o podanym tytule już istnieje")
        return False

    zadania.append(TodoTask(tytul))
    zapisz_zadania(zadania)

    if app_instance:
        app_instance.odswiez_liste_zadan()

    return True


def rozpocznij_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    for zadanie in zadania:
        if zadanie.tytul == tytul and zadanie.status == "Do zrobienia":
            zadanie.status = "W trakcie"
            zapisz_zadania(zadania)
            if app_instance:
                app_instance.odswiez_liste_zadan()
            return True

    messagebox.showwarning("Ostrzeżenie", "Nie można rozpocząć tego zadania")
    return False


def zakoncz_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    for zadanie in zadania:
        if zadanie.tytul == tytul and zadanie.status == "W trakcie":
            zadanie.status = "Wykonane"
            zapisz_zadania(zadania)
            if app_instance:
                app_instance.odswiez_liste_zadan()
            return True

    messagebox.showwarning("Ostrzeżenie", "Nie można zakończyć tego zadania")
    return False


def usun_zadanie(tytul, app_instance=None):
    zadania = zaladuj_zadania()
    nowe_zadania = [z for z in zadania if z.tytul != tytul]

    if len(nowe_zadania) < len(zadania):
        zapisz_zadania(nowe_zadania)
        if app_instance:
            app_instance.odswiez_liste_zadan()
        return True

    return False