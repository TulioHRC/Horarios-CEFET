from tkinter import filedialog
from tkinter import *
import pandas as pd
import shutil
import os

planilha = ''      # declara a variavel com algo vazio só pra ela se tornar global em btmin_click

# ==================================== função para quando o botão for apertado ===================================================
def bt_click():
    global planilha
    # interface pra escolha do arquivo
    file = filedialog.askopenfile(parent=root, mode='rb', title='abrir')
    # mostrar só o caminho do arquivo
    # print(file.name)   #.name pega só o caminho do arquivo // outro teste
    filename = file.name.split("/")
    filename1 = filename[-1] # pega o nome do arquivo

    pasta = os.path.dirname(os.path.realpath(__file__)) # pega o caminho absoluto do arquivo python que está sendo executado

    shutil.copy(file.name, './') # copia o arquivo
    #print(f"o arquivo {filename1} está em {pasta}" )  # teste

    try:
        planilha = pd.read_excel('./' + filename1)
        print(planilha)
    except Exception as e:
        print(e)


pasta = os.getcwd()
print(f"o programa está rodando em {pasta}")

root = Tk()
root.geometry('300x300+700+50',)

bt = Button(root, width=20, text='escolher arquivo', command=bt_click)
bt.place(x='70', y='100')


root.mainloop()
