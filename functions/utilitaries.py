from tkinter import messagebox
from os import startfile

def openWorksheet(path="Planilha.xlsx"):
    try:
        startfile(path)
    except Exception as e:
        messagebox.showerror("Houve um erro ao tentar abrir o arquivo", f"{e}")
