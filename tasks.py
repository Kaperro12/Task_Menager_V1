class Zadanie:
    """Podstawowa klasa reprezentująca zadanie."""
    def __init__(self, tytul, status="Do zrobienia"):
        self.tytul = tytul
        self.status = status

    def __repr__(self):
        return f"{self.tytul} ({self.status})"

# TODO: Rozszerzyć o specjalizowane klasy zadań (Todo, InProgress, Done)
# TODO: Dodać walidację danych