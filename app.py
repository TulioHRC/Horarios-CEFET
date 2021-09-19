from tkinter import *
from tkinter import ttk

def go():
    print('Criando novos horários...')

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Horários CEFET')
        self.sizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()]
        self.master.geometry(f"{int(self.sizes[0]*0.8)}x{int(self.sizes[1]*0.8)}+{int(self.sizes[0]*0.1)}+{int(self.sizes[1]*0.1)}")
        self.master.resizable(0,0)
        self.master.config(bg="Black")

        self.bt = Button(self.master, text="Criar horários", command=go, font=('Arial', 26)) # Rodará o código principal
        self.bt.config(bg="Gray", fg="White")
        self.bt.pack()
        self.bt.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.4)), height=str(int(self.sizes[1]*0.8*0.3)),
                            relx=0.3, rely=0.35)

        self.new = Button(self.master, text="Novos dados", command=AddingData, font=('Arial', 20)) # Novos dados (adicionados lá no excel)
        self.new.config(bg="Gray", fg="White")
        self.new.pack()
        self.new.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.2)), height=str(int(self.sizes[1]*0.8*0.1)),
                            relx=0.05, rely=0.85)

class AddingData(MainApp):
    def __init__(self):
        self.screen = Toplevel()
        self.screen.title('Adicionando dados')
        self.sizes = [self.screen.winfo_screenwidth(), self.screen.winfo_screenheight()]
        self.screen.geometry(f"{int(self.sizes[0]*0.6)}x{int(self.sizes[1]*0.6)}+{int(self.sizes[0]*0.2)}+{int(self.sizes[1]*0.2)}")
        self.screen.resizable(0,0)

        self.tabs = ttk.Notebook(self.screen)
        self.tabs.pack(fill=BOTH, expand=True)

        self.addTeacher = Frame(self.tabs, width=int(self.sizes[0]*0.6), bg="Black")
        self.addRoom = Frame(self.tabs, width=int(self.sizes[0]*0.6), bg="Black")

        self.addTeacher.pack(fill=BOTH, expand=True)
        self.addRoom.pack(fill=BOTH, expand=True)

        self.tabs.add(self.addTeacher, text="Nova matéria/professor")
        self.tabs.add(self.addRoom, text="Nova sala")


def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Rodando o aplicativo...')
    main()
