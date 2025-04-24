from datetime import datetime

class Zadanie:
    def __init__(self, tytul, status="Do zrobienia"):
        self.tytul = tytul
        self.status = status
        self.data_utworzenia = datetime.now()
        self.deadline = None

    def __repr__(self):
        return f"{self.tytul} ({self.status})"

    def __eq__(self, other):
        return isinstance(other, Zadanie) and self.tytul.lower() == other.tytul.lower()

class TodoTask(Zadanie):
    def __init__(self, tytul):
        super().__init__(tytul, "Do zrobienia")

class InProgressTask(Zadanie):
    def __init__(self, tytul):
        super().__init__(tytul, "W trakcie")

class DoneTask(Zadanie):
    def __init__(self, tytul):
        super().__init__(tytul, "Wykonane")