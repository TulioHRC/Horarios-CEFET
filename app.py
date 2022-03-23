from tkinter import *
from tkinter import ttk, messagebox
import os
from functions import excel
from functions import go
from functions import loadData
from functions import utilitaries

prefers = {'S': set(), 'N': set(), 'R': set()}
limits = set()
limitsRoom = set()

def start():
    print('Criando novos horários...')
    try:
        go.mainFunction()
        path = "./data"
        path = os.path.realpath(path)
        messagebox.showinfo("Horários criados", "Agora você já pode ver os horários criados, na pasta a seguir.")
        os.startfile(path)
    except Exception as e:
        messagebox.showerror("Error", f"Houve um erro ao tentar criar os horários\n{e}")

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Horários CEFET')
        self.sizes = [self.master.winfo_screenwidth(), self.master.winfo_screenheight()]
        self.master.geometry(f"{int(self.sizes[0]*0.8)}x{int(self.sizes[1]*0.8)}+{int(self.sizes[0]*0.1)}+{int(self.sizes[1]*0.1)}")
        self.master.resizable(0,0)
        self.master.config(bg="Black")

        self.configP = Button(self.master, text="Pontos", command=Points, font=('Arial', 20)) # Configurações das preferencias (para o arquivo .txt)
        self.configP.config(bg="Gray", fg="White")
        self.configP.pack()
        self.configP.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.2)), height=str(int(self.sizes[1]*0.8*0.1)),
                            relx=0.75, rely=0.05)

        self.bt = Button(self.master, text="Criar horários", command=start, font=('Arial', 26)) # Rodará o código principal
        self.bt.config(bg="Gray", fg="White")
        self.bt.pack()
        self.bt.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.4)), height=str(int(self.sizes[1]*0.8*0.3)),
                            relx=0.3, rely=0.35)

        self.new = Button(self.master, text="Novos dados", command=AddingData, font=('Arial', 20)) # Novos dados (adicionados lá no excel)
        self.new.config(bg="Gray", fg="White")
        self.new.pack()
        self.new.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.2)), height=str(int(self.sizes[1]*0.8*0.1)),
                            relx=0.05, rely=0.85)

""" Não necessário no programa atualmente, mas em futuras atualizações talvez

        self.filebt = Button(self.master, text='Escolher Arquivos', command=self.choose, font=('Arial', 20))# botão para escolher o arquivo
        self.filebt.config(bg='Gray', fg='White')
        self.filebt.pack()
        self.filebt.place(bordermode=OUTSIDE, width=str(int(self.sizes[0]*0.8*0.2)), height=str(int(self.sizes[1]*0.8*0.1)),
                            relx=0.75, rely=0.85)

    def choose (self):
        file = filedialog.askopenfile(parent=self.master, mode='rb', title='abrir')
"""

class Points(MainApp):
    def __init__(self):
        self.points = loadData.getPoints('./data/preferencias.txt')
        self.descriptions = loadData.getPoints('./data/preferencias.txt', desc=True)

        self.screen = Toplevel()
        self.screen.title("Configuração dos Pontos")
        self.sizes = [self.screen.winfo_screenwidth(), self.screen.winfo_screenheight()]
        self.screen.geometry(f"{int(self.sizes[0]*0.6)}x{int(self.sizes[1]*0.6)}+{int(self.sizes[0]*0.2)}+{int(self.sizes[1]*0.2)}")
        self.screen.resizable(0,0)
        self.screen.config(bg='Black')

        self.entries = []
        for index, point in enumerate(self.points):
            Label(self.screen, text=point, font=('Arial', 18), fg="White", bg="Gray", width=15).grid(row=index, column=0, padx=5, pady=3)
            self.entries.append(Entry(self.screen, font=('Arial', 18), justify=CENTER))
            self.entries[index].grid(row=index, column=1, padx=5, pady=2)
            self.entries[index].insert(0, self.points[point])
            Label(self.screen, text=self.descriptions[point], font=('Arial', 8), fg="White", bg="Black", width=50,
                    anchor='w').grid(row=index, column=2, padx=2, pady=3)

        Button(self.screen, text="Save", font=('Arial', 18), width=12, bg="Gray", fg="White",
                    command=self.savePrefers).grid(row=len(self.entries)+1, column=2, padx=10, pady=10)

    def savePrefers(self):
        try:
            with open('./data/preferencias.txt', 'w') as f:
                for index, prefer in enumerate(self.points):
                    f.write(f"{prefer}={self.entries[index].get()}; //{self.descriptions[prefer]}")
            messagebox.showinfo("Preferencias salvas", "As preferencias foram salvas com sucesso!!!")
            self.screen.destroy()
        except Exception as e:
            messagebox.showerror("Erro no salvamento", f"As preferencias nao foram salvas com sucesso, houve um erro durante:\n{e}")

class AddingData(MainApp):
    def __init__(self):
        global prefers, limits, limitsRoom

        prefers = {'S': set(), 'N': set(), 'R': set()}
        limits = set()
        limitsRoom = set()

        self.screen = Toplevel()
        self.screen.title('Adicionando dados')
        self.sizes = [self.screen.winfo_screenwidth(), self.screen.winfo_screenheight()]
        self.screen.geometry(f"{int(self.sizes[0]*0.6)}x{int(self.sizes[1]*0.7)}+{int(self.sizes[0]*0.2)}+{int(self.sizes[1]*0.15)}")
        self.screen.resizable(0,0)

        self.tabs = ttk.Notebook(self.screen)
        self.tabs.pack(fill=BOTH, expand=True)

        self.addTeacher()
        self.addRoom()

    def addTeacher(self):
        self.addTeacherFrame = Frame(self.tabs, width=int(self.sizes[0]*0.6), bg="Black")
        self.addTeacherFrame.pack(fill=BOTH, expand=True)
        self.tabs.add(self.addTeacherFrame, text="Nova matéria/professor")

        Label(self.addTeacherFrame, text="Nome (sem acentos):", font=('Arial', 14), bg="White").grid(row=0, column=0, padx=20, pady=10)
        self.teacherName = Entry(self.addTeacherFrame, font=('Arial', 14))
        self.teacherName.grid(row=0, column=1, padx=20, pady=10)

        Label(self.addTeacherFrame, text="Matéria (sem acentos):", font=('Arial', 14), bg="White").grid(row=1, column=0, padx=20, pady=10)
        self.teacherSubject = Entry(self.addTeacherFrame, font=('Arial', 14))
        self.teacherSubject.grid(row=1, column=1, padx=20, pady=10)

        # Tipo (manhã ou tarde)
        Label(self.addTeacherFrame, text="Tipo:", font=('Arial', 14), bg="White").grid(row=2, column=0, padx=20, pady=20)
        self.types = [
            'Manha',
            'Tarde',
        ]
        self.typeOp = StringVar()
        self.typeOp.set(self.types[0])
        self.type = OptionMenu(self.addTeacherFrame, self.typeOp, *self.types)
        self.type.grid(row=2, column=1, padx=20, pady=20)

        Label(self.addTeacherFrame, text="Ano escolar:", font=('Arial', 14), bg="White").grid(row=3, column=0, padx=20, pady=10)
        self.teacherYear = IntVar()

        options = [
        	1,
            2,
            3,
        ]

        self.teacherYear.set(1)
        self.year = OptionMenu(self.addTeacherFrame, self.teacherYear, *options)
        self.year.grid(row=3, column=1, padx=20, pady=5)

        # Bimestral?
        Label(self.addTeacherFrame, text="Bimestral?", font=('Arial', 14), bg="White").grid(row=4, column=2, padx=20, pady=10)
        self.bimestral = StringVar()
        bimestralOptions = [
            'Não',
            'Sim'
        ]

        self.bimestral.set(bimestralOptions[0])
        OptionMenu(self.addTeacherFrame, self.bimestral, *bimestralOptions).grid(row=4, column=3, padx=20, pady=10)

        # SubGrupo
        Label(self.addTeacherFrame, text="Sub-Grupo:", font=('Arial', 14), bg="White").grid(row=4, column=0, padx=20, pady=20)
        self.group = StringVar()
        groupOptions = [
            'A',
            'B',
            'C'
        ]

        self.group.set(groupOptions[0])
        OptionMenu(self.addTeacherFrame, self.group, *groupOptions).grid(row=4, column=1, padx=20, pady=5)

        Button(self.addTeacherFrame, text="Adicionar limitação", command=lambda: AddConditions('limit'),
                    font=('Arial', 18)).grid(row=1, column=2, columnspan=2, padx=20, pady=10)

        Button(self.addTeacherFrame, text="Adicionar preferência", command=lambda: AddConditions('prefer'),
                    font=('Arial', 18)).grid(row=3, column=2, columnspan=2, padx=20, pady=10)

        self.classes = Frame(self.addTeacherFrame, bg='Black')
        self.classes.grid(row=6, column=0, rowspan=2, columnspan=4, pady=10)

        self.turmasList = ['MCT', 'ELT', 'MEC']# Colocar forma de pegar a lista de turmas do CEFET
        self.classesList = {}
        columnPos = 0

        for turma in self.turmasList:
            Label(self.classes, text=f"{turma}", font=('Arial', 16), width=5, bg='Green',
                        fg='White').grid(row=0, column=columnPos, padx=1)
            self.classesList[f'{turma}'] = Entry(self.classes, font=('Arial', 16), width=5)
            self.classesList[f'{turma}'].grid(row=1, column=columnPos, padx=1, pady=0.5)

            columnPos += 1

        Button(self.addTeacherFrame, text="Criar matéria", font=('Arial', 24)
                , command=lambda: self.putInExcel('Teacher')).grid(row=8, column=1, columnspan=2, pady=10)

        Button(self.addTeacherFrame, text="Abrir planilha", command=lambda: utilitaries.openWorksheet(),
                    font=('Arial', 14)).grid(row=8, column=3, columnspan=1, padx=20, pady=10)

    def addRoom(self):
        self.addRoomFrame = Frame(self.tabs, width=int(self.sizes[0]*0.6), bg="Black")
        self.addRoomFrame.pack(fill=BOTH, expand=True)
        self.tabs.add(self.addRoomFrame, text="Nova sala")

        Label(self.addRoomFrame, text="Sala:", font=('Arial', 14), bg="White").grid(row=0, column=0, padx=20, pady=20)
        self.room = Entry(self.addRoomFrame, font=('Arial', 14), width=25)
        self.room.grid(row=0, column=1, padx=20, pady=20)

        Label(self.addRoomFrame, text="Local:", font=('Arial', 14), bg="White").grid(row=1, column=0, padx=20, pady=20)
        # List box with the locals, like 1N, 1S, 2N, etc.
        self.locals = [
            'DEMAT',
            'Andar 1 N',
            'Andar 1 S',
            'Andar 2 N',
            'Andar 2 S',
            'Andar 3 N',
            'Andar 3 S',
        ]
        self.localOption = StringVar()
        self.localOption.set(self.locals[0])
        self.local = OptionMenu(self.addRoomFrame, self.localOption, *self.locals)
        self.local.grid(row=1, column=1, padx=20, pady=20)

        Button(self.addRoomFrame, text="Adicionar limitação", command=lambda: AddConditions('limit', 1),
                    font=('Arial', 18)).grid(row=0, column=3, columnspan=2, padx=20, pady=20)

        Button(self.addRoomFrame, text="Criar sala", command=lambda: self.putInExcel('Room'),
                    font=('Arial', 18), bg="green", fg="white").grid(row=4, column=1, columnspan=3, padx=20, pady=20)

        Button(self.addRoomFrame, text="Abrir planilha", command=lambda: utilitaries.openWorksheet('Planilha sala.xlsx'),
                    font=('Arial', 14)).grid(row=4, column=3, columnspan=1, padx=20, pady=10)


    def putInExcel(self, type): # Type é sala ou professor
        global prefers, limits, limitsRoom

        if type == 'Teacher':
            turmas = {}
            for turma in self.turmasList:
                turmas[f"{turma}"] = self.classesList[f'{turma}'].get()
            try:
                excel.saveTeacher(self.teacherName.get(), self.teacherSubject.get(), self.typeOp.get(), turmas, self.teacherYear.get(), self.group.get(), 
                                    self.bimestral.get(), prefers, limits)
                messagebox.showinfo('Salvo', 'O professor foi salvo com sucesso!')
                self.screen.destroy()
            except Exception as e:
                messagebox.showerror('Erro', f'O professor não foi salvo!\n{e}')
        else:
            try:
                excel.saveRoom(self.room.get(), self.localOption.get(), limitsRoom)
                messagebox.showinfo('Salvo', 'A sala foi salva com sucesso!')
                self.screen.destroy()
            except Exception as e:
                messagebox.showerror('Erro', f'A sala não foi salva corretamente!\n{e}')


class AddConditions(AddingData):
    def __init__(self, type, room=0):
        if type == "limit": self.name = "Limitações"
        elif type == "prefer": self.name = "Preferências"

        self.screen = Toplevel()
        self.screen.title(f"Adicionando {self.name}")
        self.sizes = [self.screen.winfo_screenwidth(), self.screen.winfo_screenheight()]
        self.screen.geometry(f"{int(self.sizes[0]*0.4)}x{int(self.sizes[1]*0.3)}+{int(self.sizes[0]*0.3)}+{int(self.sizes[1]*0.3)}")

        self.tabs = ttk.Notebook(self.screen)
        self.tabs.pack(fill=BOTH, expand=True)

        self.add = Frame(self.tabs)
        self.see = Frame(self.tabs)

        self.add.pack(fill=BOTH, expand=True)
        self.see.pack(fill=BOTH, expand=True)

        self.tabs.add(self.add, text=f"Criar novas {self.name}")
        self.tabs.add(self.see, text=f"Ver {self.name}")

        self.addFrame(type, room)
        self.seeFrame(type, room)

    def addFrame(self, type, room):
        Label(self.add, text="Tipo:", font=('Arial', 18)).grid(row=0, column=0, pady=20, padx=15)
        self.type = StringVar()
        if type == 'limit':
            if room: options = ["Não pode dar aula na", "Uso especial"]
            else: options = ["Não posso dar aula na", "Tem que ser na sala"]
        else: options = ["Quero dar aula na", "Não quero dar aula na", "Prefiro na sala"]
        self.type.set(options[0])

        self.optionMenu = OptionMenu(self.add, self.type, *options, command=self.change).grid(row=0, column=1, pady=20, padx=15)

        self.frameAdd = Frame(self.add)
        self.frameAdd.grid(row=0, column=2, columnspan=3, rowspan=2, pady=20, padx=15)

        self.option = StringVar()
        dayOptions = ["segunda", "terça", "quarta", "quinta", "sexta"]
        self.option.set(dayOptions[0])

        self.menu = OptionMenu(self.frameAdd, self.option, *dayOptions).grid(row=0, column=0, pady=5, padx=5)

        Label(self.frameAdd, text="Entre os horários:").grid(row=0, column=1, pady=5, padx=2) # Horários mais especificos
        hourOptions = ["1", "2", "3", "4", "5", "6"]
        self.initialH = StringVar()
        self.initialH.set(hourOptions[0])

        self.iH = OptionMenu(self.frameAdd, self.initialH, *hourOptions).grid(row=0, column=2, pady=5, padx=2)

        self.finalH = StringVar()
        self.finalH.set(hourOptions[-1])

        self.fH = OptionMenu(self.frameAdd, self.finalH, *hourOptions).grid(row=1, column=2, pady=5, padx=2)

        Button(self.add, text="Criar", font=('Arial', 15), command=lambda: self.addP(self.type.get(), type, room)).grid(row=1, column=1, pady=10, padx=15)

    def change(self, value): # Changing the type of prefer/limit on the screen
        self.frameAdd.destroy()
        self.frameAdd = Frame(self.add)
        self.frameAdd.grid(row=0, column=2, pady=20, padx=15)
        if value[0] == 'N' or value[0] == 'Q': # S ou N prefers/limits
            self.option = StringVar()
            dayOptions = ["segunda", "terça", "quarta", "quinta", "sexta"]
            self.option.set(dayOptions[0])

            self.menu = OptionMenu(self.frameAdd, self.option, *dayOptions).grid(row=0, column=0, pady=5, padx=5)

            Label(self.frameAdd, text="Entre os horários:").grid(row=0, column=1, pady=5, padx=2)
            hourOptions = ["1", "2", "3", "4", "5", "6"]
            self.initialH = StringVar()
            self.initialH.set(hourOptions[0])

            self.iH = OptionMenu(self.frameAdd, self.initialH, *hourOptions).grid(row=0, column=2, pady=5, padx=2)

            self.finalH = StringVar()
            self.finalH.set(hourOptions[-1])

            self.fH = OptionMenu(self.frameAdd, self.finalH, *hourOptions).grid(row=1, column=2, pady=5, padx=2)
        if value[0] == 'P' or value[0] == 'T': # Preferencias de salas
            self.option = StringVar()
            roomOptions = loadData.getDatabase('Planilha sala.xlsx')['Sala']
            self.option.set(roomOptions[0])

            self.menu = OptionMenu(self.frameAdd, self.option, *roomOptions).grid(row=0, column=0, pady=5, padx=5)

            Label(self.frameAdd, text="Entre os horários:").grid(row=0, column=1, pady=5, padx=2)
            hourOptions = ["1", "2", "3", "4", "5", "6"]
            self.initialH = StringVar()
            self.initialH.set(hourOptions[0])

            self.iH = OptionMenu(self.frameAdd, self.initialH, *hourOptions).grid(row=0, column=2, pady=5, padx=2)

            self.finalH = StringVar()
            self.finalH.set(hourOptions[-1])

            self.fH = OptionMenu(self.frameAdd, self.finalH, *hourOptions).grid(row=1, column=2, pady=5, padx=2)

    def seeFrame(self, type, room):
        global prefers, limits, limitsRoom

        line = 0
        x = 40
        y = 2
        fontS = ('Arial', 14)

        if type == 'limit' and not room:
            for l in limits:
                if l[0] == 'R': t = f'Aula apenas na sala {l}'
                else: t = f"Não pode ter aula na {l}"
                Label(self.see, text=t, font=fontS, fg="#855862").grid(row=line, column=0, columnspan=2, padx=x, pady=y)
                Button(self.see, text="Excluir", font=fontS, command=lambda: self.delete(type, limits, l, room)).grid(row=line, column=2, padx=x, pady=y)
                line += 1
        elif type == 'limit' and room:
            for l in limitsRoom:
                if l == 'ESPECIFICA': t = 'Uso especial'
                else: t = f"Não pode ter aula na {l}"
                Label(self.see, text=t, font=fontS, fg="#855862").grid(row=line, column=0, columnspan=2, padx=x, pady=y)
                Button(self.see, text="Excluir", font=fontS, command=lambda: self.delete(type, limitsRoom, l, room)).grid(row=line, column=2, padx=x, pady=y)
                line += 1
        else:
            for p in prefers['S']:
                Label(self.see, text=f"Quero dar aula na {p}", font=fontS, fg="#59915c").grid(row=line, column=0, columnspan=2, padx=x, pady=y)
                Button(self.see, text="Excluir", font=fontS, command=lambda: self.delete(type, prefers["S"], p, room)).grid(row=line, column=2, padx=x, pady=y)
                line += 1
            for p in prefers['N']:
                Label(self.see, text=f"Não quero dar aula na {p}", font=fontS, fg="#855862").grid(row=line, column=0, columnspan=2, padx=x, pady=y)
                Button(self.see, text="Excluir", font=fontS, command=lambda: self.delete(type, prefers["N"], p, room)).grid(row=line, column=2, padx=x, pady=y)
                line += 1
            for p in prefers['R']:
                Label(self.see, text=f"Prefiro dar aula na sala {p}", font=fontS).grid(row=line, column=0, columnspan=2, padx=x, pady=y)
                Button(self.see, text="Excluir", font=fontS, command=lambda: self.delete(type, prefers["R"], p, room)).grid(row=line, column=2, padx=x, pady=y)
                line += 1

    def delete(self, type, setList, day, room=0):
        setList.remove(day)
        self.screen.destroy()
        AddConditions(type, room)

    def addP(self, typeOption, type, room=0):
        global prefers, limits, limitsRoom

        if type == "limit" and not room:
            if typeOption[0] == 'N' or typeOption[0] == 'Q': # S/N prefers
                if not self.option.get() in prefers['S']:
                    limits.add(self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())
                else:
                    messagebox.showerror('Este dia já é uma preferencia', 'Se você quiser adicionar esta limitação, exclua a preferencia primeiramente.')
            elif typeOption[0] == 'P' or typeOption[0] == 'T': # Room preferences
                if not 'R' in str(limits):
                    limits.add('R' + self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())
                else:
                    messagebox.showerror('Já há uma limitação de sala', 'Se você quiser adicionar esta limitação, exclua a outra limitação de sala primeiramente.')

        elif type == "limit" and room:
            if typeOption[0] == 'U':
                limitsRoom.add('ESPECIFICA')
            else: limitsRoom.add(self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())

        else: # Prefers
            if self.type.get() == "Quero dar aula na":
                if not self.option.get() in limits:
                    prefers['S'].add(self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())
                else:
                    messagebox.showerror('Este dia já é uma limitação', 'Se você quiser adicionar esta limitação, exclua a limitação primeiramente.')
            elif typeOption[0] == "N":
                prefers['N'].add(self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())
            else:
                prefers['R'].add(self.option.get() + ';' + self.initialH.get() + ',' + self.finalH.get())
        self.screen.destroy()
        AddConditions(type, room)


def main():
    root = Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    print('Rodando o aplicativo...')
    main()
