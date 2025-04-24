# Menedżer Zadań v1.0

Aplikacja do zarządzania zadaniami z podziałem na statusy: **Do zrobienia**, **W trakcie**, **Wykonane**. Ułatwia organizację pracy i śledzenie postępów.

## ✨ Funkcje

- ✅ **Dodawanie zadań** z opcjonalnym terminem wykonania  
- ✏️ **Edytowanie** istniejących zadań  
- 🔄 **Zmiana statusu** zadania (rozpoczęcie/zakończenie)  
- 🗑️ **Usuwanie** zadań  
- 🎨 **Automatyczne kolorowanie** zadań według statusu i terminów  
- 📊 **Statystyki** wykonanych zadań  
- 💾 **Eksport** danych do pliku CSV  

## 🛠 Wymagania systemowe

- Python 3.x  
- Biblioteki:  
  - `tkinter` (standardowa biblioteka GUI dla Pythona)  
  - `openpyxl` (do obsługi plików Excel)

## 🚀 Instalacja

1. Pobierz pliki programu:
   - `main.py`
   - `tasks.py`
   - `functions.py`

2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install openpyxl
   ```

## ▶️ Uruchomienie

Wykonaj w terminalu:
```bash
python main.py
```

## ⌨️ Skróty klawiszowe

| Skrót       | Działanie             |
|-------------|------------------------|
| Ctrl+N      | Dodaj nowe zadanie     |
| Ctrl+D      | Edytuj zadanie         |
| Ctrl+E      | Eksport do CSV         |
| Ctrl+Q      | Wyjście z programu     |
| Enter       | Potwierdź dodawanie    |

## 📁 Struktura plików

- `Tasks.xlsx` – główny plik przechowujący zadania (tworzony automatycznie)
- `tasks_export.csv` – plik eksportu zadań (tworzony na żądanie)

---

> Projekt w wersji 1.0 – idealny do osobistego zarządzania zadaniami w prosty i przejrzysty sposób.
