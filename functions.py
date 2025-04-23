import openpyxl
from openpyxl.styles import PatternFill
from tasks import TodoTask

NAZWA_PLIKU = "Tasks.xlsx"
KOLORY = {
    "Do zrobienia": "#FF9999",
    "W trakcie": "#FFFF99",
    "Wykonane": "#99FF99"
}


def sprawdz_lub_utworz_plik():
    """Sprawdza istnienie pliku Excel lub tworzy nowy z nagłówkami."""
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
    """Ładuje listę zadań z pliku Excel."""
    skoroszyt = sprawdz_lub_utworz_plik()
    arkusz = skoroszyt.active
    zadania = []

    for wiersz in arkusz.iter_rows(min_row=2, values_only=True):
        tytul, status = wiersz
        if status == "Do zrobienia":
            zadania.append(TodoTask(tytul))
        # TODO: Obsłużyć inne statusy zadań

    return zadania


def dodaj_zadanie(tytul):
    """Dodaje nowe zadanie do pliku."""
    zadania = zaladuj_zadania()
    zadania.append(TodoTask(tytul))
    zapisz_zadania(zadania)


def zapisz_zadania(zadania):
    """Zapisuje listę zadań do pliku Excel."""
    skoroszyt = openpyxl.Workbook()
    arkusz = skoroszyt.active
    arkusz.title = "Tasks"
    arkusz.append(["Title", "Status"])

    for zadanie in zadania:
        arkusz.append([zadanie.tytul, zadanie.status])

    skoroszyt.save(NAZWA_PLIKU)

# TODO: Dodać funkcje zmiany statusu zadań
# TODO: Dodać formatowanie komórek Excel