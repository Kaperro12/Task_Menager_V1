import tkinter as tk
from tkinter import ttk


# TODO: Importować funkcje pomocnicze gdy będą gotowe
# TODO: Zaimplementować główną klasę aplikacji

def main():
    root = tk.Tk()
    root.title("Menedżer Zadań - Wersja Początkowa")
    root.geometry("400x300")

    # TODO: Dodać podstawowy interfejs użytkownika
    label = ttk.Label(root, text="To będzie menedżer zadań")
    label.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()