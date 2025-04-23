import openpyxl

# Stałe
NAZWA_PLIKU = "Tasks.xlsx"

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

# TODO: Zaimplementować funkcję ładowania zadań
# TODO: Dodać funkcje zarządzania zadaniami (dodawanie, zmiana statusu)