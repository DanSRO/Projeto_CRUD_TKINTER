import re
import sqlite3
import tkinter as tk
import tkinter.ttk as tkk
from tkinter import messagebox


class ConectarDB:
    def __init__(self):
        self.con = sqlite3.connect('db.alunos')
        self.cur = self.con.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        try:
            # self.cur.execute('''CREATE TABLE IF NOT EXISTS tabela_alunos (
            #     cpf TEXT PRIMARY KEY NOT NULL,
            #     nome TEXT NOT NULL,
            #     data_nasc TEXT NOT NULL,
            #     sexo TEXT NOT NULL,
            #     idade TEXT NOT NULL,
            #     av1 INTEGER NOT NULL,
            #     av2 INTEGER NOT NULL,
            #     media REAL NOT NULL
            #     )''')
            self.cur.execute('''CREATE TABLE IF NOT EXISTS tabela_alunos (
                cpf TEXT PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL,
                data_nasc TEXT NOT NULL
                )''')
        except Exception as e:
            print('[x] Falha ao criar tabela: %s [x]' % e)
        else:
            print('\n[!] Tabela criada com sucesso [!]\n')

    def inserir_registro(self, ncpf, nnome, ndata_nasc):
    # def inserir_registro(self, ncpf, nnome, ndata_nasc, nsexo, nidade, nav1, nav2, nmedia):
        try:
            self.cur.execute(
                '''INSERT INTO tabela_alunos VALUES (?, ?, ?)''', (ncpf, nnome, ndata_nasc))
                # '''INSERT INTO tabela_alunos VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (ncpf, nnome, ndata_nasc, nsexo, nidade, nav1, nav2,nmedia))
        except Exception as e:
            print('\n[x] Falha ao inserir registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro inserido com sucesso [!]\n')

    def consultar_registros(self):
        return self.cur.execute('SELECT rowid, * FROM tabela_alunos').fetchall()

    def consultar_ultimo_rowid(self):
        return self.cur.execute('SELECT MAX(rowid) FROM tabela_alunos').fetchone()

    def remover_registro(self, rowid):
        try:
            self.cur.execute("DELETE FROM tabela_alunos WHERE rowid=?", (rowid,))
        except Exception as e:
            print('\n[x] Falha ao remover registro [x]\n')
            print('[x] Revertendo operação (rollback) %s [x]\n' % e)
            self.con.rollback()
        else:
            self.con.commit()
            print('\n[!] Registro removido com sucesso [!]\n')


class Janela(tk.Frame):
    """Janela principal"""

    def __init__(self, master=None):
        """Construtor"""
        super().__init__(master)
        # Coletando informações do monitor
        largura = round(self.winfo_screenwidth() / 2)
        altura = round(self.winfo_screenheight() / 2)
        tamanho = ('%sx%s' % (largura, altura))

        # Título da janela principal.
        master.title('Cadastro de Alunos')

        # Tamanho da janela principal.
        master.geometry(tamanho)

        # Instanciando a conexão com o banco.
        self.banco = ConectarDB()

        # Gerenciador de layout da janela principal.
        self.pack()

        # Criando os widgets da interface.
        self.criar_widgets()

    def criar_widgets(self):
        # Containers.
        frame1 = tk.Frame(self)
        frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5)

        frame2 = tk.Frame(self)
        frame2.pack(fill=tk.BOTH, expand=True)

        frame3 = tk.Frame(self)
        frame3.pack(side=tk.BOTTOM, padx=5)
        
        # frame3 = tk.Frame(self)
        # frame3.pack(side=tk.BOTTOM, padx=5)
        # frame3 = tk.Frame(self)
        # frame3.pack(side=tk.BOTTOM, padx=5)
        # frame3 = tk.Frame(self)
        # frame3.pack(side=tk.BOTTOM, padx=5)
        # frame3 = tk.Frame(self)
        # frame3.pack(side=tk.BOTTOM, padx=5)
        # frame3 = tk.Frame(self)
        # frame3.pack(side=tk.BOTTOM, padx=5)

        # Labels.
        label_cpf = tk.Label(frame1, text='N° CPF')
        label_cpf.grid(row=0, column=0)

        label_nome = tk.Label(frame1, text='Aluno')
        label_nome.grid(row=0, column=1)

        label_data_nasc = tk.Label(frame1, text='Data recebimento')
        label_data_nasc.grid(row=0, column=2)
        
        # label_sexo = tk.Label(frame1, text='Sexo')
        # label_sexo.grid(row=0, column=3)
        
        # label_idade = tk.Label(frame1, text='Idade')
        # label_idade.grid(row=0, column=4)
        
        # label_av1 = tk.Label(frame1, text='Av1')
        # label_av1.grid(row=0, column=5)
        
        # label_av2 = tk.Label(frame1, text='Av2')
        # label_av2.grid(row=0, column=6)
        
        # label_media = tk.Label(frame1, text='Média')
        # label_media.grid(row=0, column=7)

        # Entrada de texto.
        self.entry_cpf = tk.Entry(frame1)
        self.entry_cpf.grid(row=1, column=0)

        self.entry_nome = tk.Entry(frame1)
        self.entry_nome.grid(row=1, column=1, padx=10)

        self.entry_data_nasc = tk.Entry(frame1)
        self.entry_data_nasc.grid(row=1, column=2)
        
        # self.entry_sexo = tk.Entry(frame1)
        # self.entry_sexo.grid(row=1, column=3)
        
        # self.entry_idade = tk.Entry(frame1)
        # self.entry_idade.grid(row=1, column=4)
        
        # self.entry_av1 = tk.Entry(frame1)
        # self.entry_av1.grid(row=1, column=5)
        
        # self.entry_av2 = tk.Entry(frame1)
        # self.entry_av2.grid(row=1, column=6)
        
        # self.entry_media = tk.Entry(frame1)
        # self.entry_media.grid(row=1, column=7)

        # Botão para adicionar um novo registro.
        button_adicionar = tk.Button(frame1, text='Adicionar', bg='blue', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_adicionar['command'] = self.adicionar_registro
        button_adicionar.grid(row=0, column=3, rowspan=2, padx=10)

        # Treeview.
        self.treeview = tkk.Treeview(frame2, columns=('N° CPF', 'Nome', 'Data de Nascimento'))
        self.treeview.heading('#0', text='ROWID')
        self.treeview.heading('#1', text='N° CPF')
        self.treeview.heading('#2', text='Nome')
        self.treeview.heading('#3', text='Data de Nascimento')
        # self.treeview.heading('#2', text='Sexo')
        # self.treeview.heading('#2', text='Idade')
        # self.treeview.heading('#2', text='Av1')
        # self.treeview.heading('#2', text='Av2')
        # self.treeview.heading('#2', text='Média')

        # Inserindo os dados do banco no treeview.
        for row in self.banco.consultar_registros():
            self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3]))
            # self.treeview.insert('', 'end', text=row[0], values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Botão para remover um item.
        button_excluir = tk.Button(frame3, text='Excluir', bg='red', fg='white')
        # Método que é chamado quando o botão é clicado.
        button_excluir['command'] = self.excluir_registro
        button_excluir.pack(pady=10)

    def adicionar_registro(self):
        # Coletando os valores.
        cpf = self.entry_cpf.get()
        nome = self.entry_nome.get()
        data_nasc = self.entry_data_nasc.get()
        # sexo = self.entry_sexo.get()
        # idade = self.entry_idade.get()
        # av1 = self.entry_av1.get()
        # av2 = self.entry_av2.get()
        # media = self.entry_media.get()

        # Validação simples (utilizar datetime deve ser melhor para validar).
        validar_data = re.search(r'(..)/(..)/(....)', data_nasc)

        # Se a data digitada passar na validação
        if validar_data:
            # Dados digitando são inseridos no banco de dados
            self.banco.inserir_registro(ncpf=cpf, nnome=nome, ndata_nasc=data_nasc)
            # self.banco.inserir_registro(ncpf=cpf, nnome=nome, ndata_nasc=data_nasc, nsexo=sexo, nidade=idade, nav1=av1, nav2=av2, nmedia=media)

            # Coletando a ultima rowid que foi inserida no banco.
            rowid = self.banco.consultar_ultimo_rowid()[0]

            # Adicionando os novos dados no treeview.
            self.treeview.insert('', 'end', text=rowid, values=(cpf, nome, data_nasc))
            # self.treeview.insert('', 'end', text=rowid, values=(cpf, nome, data_nasc, idade, sexo, av1, av2, media))
        else:
            # Caso a data não passe na validação é exibido um alerta.
            messagebox.showerror('Erro', 'Padrão de data incorreto, utilize dd/mm/yyyy')

    def excluir_registro(self):
        # Verificando se algum item está selecionado.
        if not self.treeview.focus():
            messagebox.showerror('Erro', 'Nenhum item selecionado')
        else:
            # Coletando qual item está selecionado.
            item_selecionado = self.treeview.focus()

            # Coletando os dados do item selecionado (dicionário).
            rowid = self.treeview.item(item_selecionado)

            # Removendo o item com base no valor do rowid (argumento text do treeview).
            # Removendo valor da tabela.
            self.banco.remover_registro(rowid['text'])

            # Removendo valor do treeview.
            self.treeview.delete(item_selecionado)


root = tk.Tk()
app = Janela(master=root)
app.mainloop()