class Zadanie:
    """Podstawowa klasa reprezentująca zadanie."""
    def __init__(self, tytul, status="Do zrobienia"):
        self.tytul = tytul
        self.status = status

    def __repr__(self):
        return f"{self.tytul} ({self.status})"

class TodoTask(Zadanie):
    """Zadanie do wykonania."""
    def __init__(self, tytul):
        super().__init__(tytul, "Do zrobienia")

# TODO: Dodać klasy InProgressTask i DoneTask
# TODO: Dodać walidację danych