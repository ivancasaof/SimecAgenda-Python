from tkinter import *
import customtkinter, time
from PIL import ImageTk, Image
from tkinter import ttk, messagebox
from ldap3 import *
from tkcalendar import *
from datetime import datetime, timedelta, date
import mysql.connector
#// Cores
cor_primaria = '#1D366C'
cor_primaria2 = '#2C7EEA'
cor_secundaria = '#6C757D'
cor_faded = '#f7f7f7'
cor_branca = '#ffffff'
cor_cfraca = '#eeeeee'
cor_danger = '#DC3545'
cor_orange = '#E77E23'
#// Fontes
ft_padrao = ("Calibri",12)
ft_padrao_bold = ("Calibri Bold",12)
ft_titulo = ("Calibri",16)
ft_titulo_janelas = ("Calibri Bold",16)

#// Variaveis Globais
usuario_logado = ''
titulos = 'Simec Agenda: 1.1'
dthoje = time.strftime('%d/%m/%Y', time.localtime())
data_hoje = datetime.strptime(str(dthoje), "%d/%m/%Y")

#// Botoes
bt_padrao = {'fg_color':cor_branca, 'hover_color':cor_faded, 'text_font':ft_padrao, 'text_color':cor_primaria }
bt_confirma1 = {'fg_color':cor_primaria2, 'hover_color':cor_primaria2, 'text_font':ft_padrao, 'text_color':cor_branca }
bt_cancela1= {'fg_color':cor_danger, 'hover_color':cor_danger, 'text_font':ft_padrao, 'text_color':cor_branca }
bt_edita1= {'fg_color':cor_orange, 'hover_color':cor_orange, 'text_font':ft_padrao, 'text_color':cor_branca }
bt_icone = {'background':cor_branca, 'borderwidth':0, 'highlightthickness':0, 'relief':RIDGE, 'activebackground':"#ffffff", 'activeforeground':"#7c7c7c", 'cursor':"hand2"}
opt_menu = {'fg_color':'#EEEEEE', 'button_color':cor_cfraca, 'button_hover_color':cor_cfraca, 'text_font':ft_padrao, 'text_color':cor_secundaria, 'dropdown_color':cor_branca, 'dropdown_hover_color':cor_cfraca, 'dropdown_text_color':cor_secundaria, 'dropdown_text_font':ft_padrao, 'corner_radius':8}
ent_padrao = {'fg_color':cor_branca, 'text_color':cor_secundaria, 'placeholder_text_color':cor_secundaria, 'text_font':ft_padrao, 'border_color':cor_secundaria, 'border_width':2, 'corner_radius':8}
ent_padrao_form = {'fg_color':cor_branca, 'text_color':cor_secundaria, 'placeholder_text_color':cor_secundaria, 'text_font':ft_padrao, 'border_color':cor_secundaria, 'border_width':2, 'corner_radius':8, 'justify':'center'}
#// Funcoes
def sair():
    root.destroy()

def lista_contatos():
    for widget in frame4.winfo_children():
            widget.destroy()
    #// Funcoes
    
    def atualiza_lista():
        tree_contatos.delete(*tree_contatos.get_children())
        cont = 0
        for i in range(len(lista)):
            if lista[i]['ramal'] != '' and lista[i]['email'] != '':
                if cont % 2 == 0:
                    tree_contatos.insert('', 'end', text=" ",
                                            values=(
                                            lista[i]['name'], lista[i]['email'], lista[i]['ramal'], lista[i]['setor']),
                                            tags=('par',))
                else:
                    tree_contatos.insert('', 'end', text=" ",
                                            values=(
                                            lista[i]['name'], lista[i]['email'], lista[i]['ramal'], lista[i]['setor']),
                                            tags=('impar',))
                cont += 1
    
    def busca_bind(event):
        busca()
    
    def busca():
        if clique_option.get() == 'Nome':
            busca = ent_busca.get().lower().capitalize()
            valor_busca = 'name'
        elif clique_option.get() == 'E-mail':
            busca = ent_busca.get().lower()
            valor_busca = 'email'
        elif clique_option.get() == 'Ramal':
            busca = ent_busca.get().lower()
            valor_busca = 'ramal'        
        elif clique_option.get() == 'Setor':
            busca = ent_busca.get().lower().capitalize()
            valor_busca = 'setor'                
        tree_contatos.delete(*tree_contatos.get_children())
        for i in range(len(lista)):
            if busca in lista[i][valor_busca]:
                cont = 0
                if lista[i]['ramal'] != '' and lista[i]['email'] != '':
                    if cont % 2 == 0:
                        tree_contatos.insert('', 'end', text=" ",
                                                values=(
                                                lista[i]['name'], lista[i]['email'], lista[i]['ramal'], lista[i]['setor']),
                                                tags=('par',))
                    else:
                        tree_contatos.insert('', 'end', text=" ",
                                                values=(
                                                lista[i]['name'], lista[i]['email'], lista[i]['ramal'], lista[i]['setor']),
                                                tags=('impar',))
                    cont += 1
        
    conn = Connection("192.168.1.20", "gvdobrasil\\impressoras", "gv2K17ADM", auto_bind=True)
    conn.search('DC=gvdobrasil,DC=local',
                        "(&(objectClass=person)(objectClass=user)(sAMAccountType=805306368)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))",
                        SUBTREE, attributes=['sAMAccountName', 'displayName', 'physicalDeliveryOfficeName', 'mail', 'postalCode'])
    lista = []
    for i in conn.entries:
        #result = '{0} {1}'.format(i.sAMAccountName.values, i.displayName.values)
        conta_nome = format(i.sAMAccountName.values[0])
        display_nome = format(i.displayName.values)
        limpa_nome = display_nome.translate({ord(i): None for i in "['],"})
        setor = format(i.physicalDeliveryOfficeName.values)
        limpa_setor = setor.translate({ord(i): None for i in "['],"})
        email = format(i.mail.values)
        limpa_email = email.translate({ord(i): None for i in "['],"})
        ramal = format(i.postalCode.values)
        limpa_ramal = ramal.translate({ord(i): None for i in "['],"})
        lista.append({'name': limpa_nome, 'nome_conta': conta_nome, 'setor': limpa_setor, 'email': limpa_email, 'ramal': limpa_ramal})

    #// Layout
    fr1 = Frame(frame4, bg='#ffffff')
    fr1.pack(side=TOP, fill=X)
    fr2 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr2.pack(padx=0, pady=(2,10), fill="x", expand=False, side=TOP)
    fr3 = Frame(frame4, bg='#ffffff')
    fr3.pack(side=TOP, fill=BOTH, expand=True, padx=20)

    #// Frame1
    img_phone = Image.open('img\\phone.png')
    resize_phone = img_phone.resize((30, 30))
    nova_img_phone = ImageTk.PhotoImage(resize_phone)
    lbl_phone = Label(fr1, image=nova_img_phone, text=' Lista de Contatos', font=ft_titulo, compound='left', background=cor_branca, fg=cor_primaria)
    lbl_phone.photo = nova_img_phone
    lbl_phone.grid(row=0, column=0, padx=20)

    clique_option = StringVar()
    lista_area = ['Nome', 'E-mail', 'Ramal', 'Setor']
    opt_option = customtkinter.CTkOptionMenu(fr1, variable=clique_option, values=lista_area, width=150, height=25, **opt_menu)
    opt_option.grid(row=0, column=2, padx=0)
    opt_option.set('Nome')

    img_lupa = Image.open('img\\lupa.png')
    resize_lupa = img_lupa.resize((20, 20))
    nova_img_lupa = ImageTk.PhotoImage(resize_lupa)
    bt_lupa = Button(fr1, image=nova_img_lupa, **bt_icone, command=busca)
    bt_lupa.photo = nova_img_lupa
    bt_lupa.grid(row=0, column=3, padx=4)

    ent_busca = customtkinter.CTkEntry(fr1, width=150, height=25, placeholder_text='Procurar', **ent_padrao, textvariable=busca) 
    ent_busca.grid(row=0, column=4, padx=(0,20))       
    ent_busca.bind("<Return>", busca_bind)
    fr1.grid_columnconfigure(1, weight=1) 

    #// Frame2 Linha

    #// Frame3
    style = ttk.Style()
    #style.theme_use('default')
    style.configure('Treeview',
                    background=cor_branca,
                    rowheight=24,
                    fieldbackground=cor_branca,
                    font=ft_padrao)
    style.configure("Treeview.Heading",
                    foreground=cor_primaria,
                    background=cor_branca,
                    height=200,
                    font=ft_padrao)
    style.map('Treeview', background=[('selected', cor_primaria)])

    tree_contatos = ttk.Treeview(fr3, selectmode='none')
    vsb = ttk.Scrollbar(fr3, orient="vertical", command=tree_contatos.yview)
    vsb.pack(side=RIGHT, fill='y')
    tree_contatos.configure(yscrollcommand=vsb.set)
    vsbx = ttk.Scrollbar(fr3, orient="horizontal", command=tree_contatos.xview)
    vsbx.pack(side=BOTTOM, fill='x')
    tree_contatos.configure(xscrollcommand=vsbx.set)
    tree_contatos.pack(side=LEFT, fill=BOTH, expand=True, anchor='n')
    tree_contatos["columns"] = ("1", "2", "3", "4")
    tree_contatos['show'] = 'headings'
    tree_contatos.column("1", anchor='c', width=80)
    tree_contatos.column("2", anchor='c')
    tree_contatos.column("3", anchor='c')
    tree_contatos.column("4", anchor='c')
    tree_contatos.heading("1", text="Nome")
    tree_contatos.heading("2", text="E-mail")
    tree_contatos.heading("3", text="Ramal")
    tree_contatos.heading("4", text="Setor")
    tree_contatos.tag_configure('par', background=cor_cfraca)
    tree_contatos.tag_configure('impar', background=cor_branca)
   
    atualiza_lista()

def agendar():
    for widget in frame4.winfo_children():
            widget.destroy()
    #// Funcoes
    def atualiza_lista():
        db.cmd_reset_connection()
        tree_agenda.delete(*tree_agenda.get_children())
        cursor.execute("SELECT * from agendas order by data, sala, hora_inicio")
        cont = 0
        for row in cursor:
            data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
            if data_banco >= data_hoje:
                if cont % 2 == 0:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('par',))
                else:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('impar',))
                cont += 1

    def busca_bind(event):
        busca()
    
    def busca():
        opt = opt_busca.get()
        db.cmd_reset_connection()
        tree_agenda.delete(*tree_agenda.get_children())    #LIKE '%21/11%'
        if opt == 'Data':
            busca = ent_busca.get()
            query = "SELECT * FROM agendas where data LIKE '%"+busca+"%' order by sala, hora_inicio"
            cursor.execute(query)
        elif opt == 'Sala':
            busca = ent_busca.get()
            query = "SELECT * FROM agendas where sala LIKE '%"+busca+"%' order by sala, hora_inicio"
            cursor.execute(query)            
        cont = 0
        for row in cursor:
            data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
            if data_banco >= data_hoje:
                if cont % 2 == 0:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('par',))
                else:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('impar',))
                cont += 1

    def calendario():
        root2 = Toplevel(root)
        window_width = 360
        window_height = 258
        screen_width = root2.winfo_screenwidth()
        screen_height = root2.winfo_screenheight() - 70
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        root2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        root2.resizable(0, 0)
        root2.configure(bg='#ffffff')
        root2.title(titulos)
        root2.overrideredirect(True)
        root2.focus_force()
        root2.grab_set()

        def escolher_data_bind(event):
            escolher_data()
        def escolher_data():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.insert(0, cal.get_date())
            ent_data.configure(state='readonly')
            root2.destroy()
            root.focus_force()
            root.grab_set()
            filtro_escolha()
        
        hoje = date.today()
        cal = Calendar(root2, font=ft_padrao, selectmode='day', locale='pt_BR',
                   mindate=hoje, cursor="hand1", background=cor_primaria2, foreground=cor_branca, bordercolor=cor_primaria2, headersbackground=cor_cfraca, headersforeground=cor_secundaria )
        
        cal.pack(fill="both", expand=True)
    
        root2.bind('<Double-1>',escolher_data_bind) # Escolhe a data ao clicar 2x com o mouse
        root2,mainloop()

    def filtro_escolha():
        db.cmd_reset_connection()
        tree_agenda.delete(*tree_agenda.get_children())    
        data = ent_data.get()
        sala = opt_sala.get()    
        if sala != '':
            cursor.execute("SELECT * FROM agendas where data = %s and sala = %s order by data, sala, hora_inicio",(data,sala,))
        else:
            cursor.execute("SELECT * FROM agendas where data = %s order by data, sala, hora_inicio",(data,))            
        cont = 0
        for row in cursor:
            data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
            if data_banco >= data_hoje:
                if cont % 2 == 0:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('par',))
                else:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('impar',))
                cont += 1

    def filtro_escolha_sala(event):
        db.cmd_reset_connection()
        tree_agenda.delete(*tree_agenda.get_children())    
        data = ent_data.get()
        sala = opt_sala.get()    
        if data != '':
            cursor.execute("SELECT * FROM agendas where data = %s and sala = %s order by data, sala, hora_inicio",(data,sala,))
        else:
            cursor.execute("SELECT * FROM agendas where sala = %s order by data, sala, hora_inicio",(sala,))            
        cont = 0
        for row in cursor:
            data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
            if data_banco >= data_hoje:
                if cont % 2 == 0:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('par',))
                else:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                            tags=('impar',))
                cont += 1

    def salvar():
        def confirmacao():
            try:
                cursor.execute("INSERT INTO agendas (\
                    data,\
                    titulo,\
                    hora_inicio,\
                    hora_fim,\
                    sala,\
                    usuario)\
                    values(%s,%s,%s,%s,%s,%s)", (data_agenda, titulo, hora_inicio, hora_fim, sala, usuario))
                db.commit()
            except:
                messagebox.showerror('Simec Agenda', 'Erro de conexão com o Banco de Dados.', parent=root)
                return False
            messagebox.showinfo('Simec Agenda', 'Reunião agendada com sucesso.', parent=root)
            agendar()

        titulo = ent_titulo.get().upper()
        data_agenda = ent_data.get()
        hora_inicio = clique_inicio.get()
        hora_fim = clique_fim.get()
        sala = clique_sala.get()
        usuario = usuario_logado
        if titulo == '' or  data_agenda == '' or hora_inicio == '' or hora_fim == '' or sala == '':
            messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root)
        else:
            cursor.execute("SELECT * from agendas where data = %s and sala = %s order by hora_inicio, sala",(data_agenda,sala,))
            resultado = cursor.fetchall()

            time_selec_inicio = datetime.strptime(str(opt_option_ini.get()),"%H:%M:%S")
            time_selec_fim = datetime.strptime(str(opt_option_fim.get()),"%H:%M:%S")

            if len(resultado) == 0:
                if time_selec_inicio == time_selec_fim:
                    messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                elif time_selec_inicio > time_selec_fim:
                    messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                else:
                    confirmacao()
            else:
                if time_selec_inicio == time_selec_fim:
                    messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                elif time_selec_inicio > time_selec_fim:
                    messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                else:
                    for r in resultado:
                        inicio = r[3]
                        fim = r[4]
                        time_bd_inicio = datetime.strptime(str(inicio),"%H:%M:%S")
                        time_bd_fim = datetime.strptime(str(fim),"%H:%M:%S")        

                        time_selec_inicio = datetime.strptime(str(opt_option_ini.get()),"%H:%M:%S")
                        time_selec_fim = datetime.strptime(str(opt_option_fim.get()),"%H:%M:%S")
                        confirma = True
                        if (time_selec_inicio >= time_bd_inicio and time_selec_inicio < time_bd_fim) or (time_selec_fim > time_bd_inicio and time_selec_fim <= time_bd_fim) or (time_selec_inicio < time_bd_inicio and time_selec_fim >= time_bd_fim):
                            confirma = False
                            break
                    if confirma == True:
                        confirmacao()
                    else:
                        messagebox.showwarning('Simec Agenda', 'Intervalo de horário indisponível.', parent=root)

    def excluir():
        lista_select = tree_agenda.focus()
        if lista_select == "":
            messagebox.showwarning('Simec Agenda:', 'Selecione a reunião que deseja excluir.', parent=root)
        else:
            valor_lista = tree_agenda.item(lista_select, "values")[0]
            
            cursor.execute("select usuario from agendas where id = %s",(valor_lista,))
            usuario_bd = cursor.fetchone()[0]
            if usuario_bd != usuario_logado:
                messagebox.showwarning('Simec Agenda:', 'Não é permitido excluir a reunião de outro usuário!', parent=root)
            else:
                resp = messagebox.askyesno('Simec Agenda:', 'Confirma a exclusão desta reunião?', parent=root)
                if resp:
                    try:
                        cursor.execute("DELETE from agendas where id = %s",(valor_lista,))
                        db.commit()
                    except:
                        messagebox.showerror('Simec Agenda:', 'Erro de conexão com o Banco de Dados.', parent=root)
                        return False
                    messagebox.showinfo('Simec Agenda:', 'Reunião excluída com sucesso.', parent=root)
                    agendar()

    def editar():
        def setup_editar():
            ent_titulo.delete(0, END)
            ent_titulo.insert(0, resultado[2])
            
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.insert(0, resultado[1])
            ent_data.configure(state='readonly')

            opt_option_ini.set(resultado[3])
            opt_option_fim.set(resultado[4])

            opt_sala.set(resultado[5])

        def confirma_edicao():
            def confirmacao():
                try:
                    cursor.execute("UPDATE agendas SET\
                        data = %s,\
                        titulo = %s,\
                        hora_inicio = %s,\
                        hora_fim = %s,\
                        sala = %s\
                        WHERE id = %s", (data_agenda, titulo, hora_inicio, hora_fim, sala, resultado[0]))
                    db.commit()
                except:
                    messagebox.showerror('Simec Agenda:', 'Erro de conexão com o Banco de Dados.', parent=root)
                    return False
                messagebox.showinfo('Simec Agenda:', 'Reunião editada com sucesso.', parent=root)
                agendar()

            titulo = ent_titulo.get().upper()
            data_agenda = ent_data.get()
            hora_inicio = clique_inicio.get()
            hora_fim = clique_fim.get()
            sala = clique_sala.get()

            if titulo == '' or  data_agenda == '' or hora_inicio == '' or hora_fim == '' or sala == '':
                messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root)
            else:
                if hora_inicio != resultado[3] or hora_fim != resultado[4] or sala != resultado[5]:
                    cursor.execute("SELECT * from agendas where data = %s and sala = %s order by hora_inicio, sala",(data_agenda,sala,))
                    resultado_db = cursor.fetchall()

                    time_selec_inicio = datetime.strptime(str(opt_option_ini.get()),"%H:%M:%S")
                    time_selec_fim = datetime.strptime(str(opt_option_fim.get()),"%H:%M:%S")

                    if len(resultado_db) == 0:
                        if time_selec_inicio == time_selec_fim:
                            messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                        elif time_selec_inicio > time_selec_fim:
                            messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                        else:
                            confirmacao()
                    else:
                        if time_selec_inicio == time_selec_fim:
                            messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                        elif time_selec_inicio > time_selec_fim:
                            messagebox.showwarning('Simec Agenda', 'Intervalo de horário inválido.', parent=root)
                        else:
                            for r in resultado_db:
                                inicio = r[3]
                                fim = r[4]
                                id = r[0]
                                time_bd_inicio = datetime.strptime(str(inicio),"%H:%M:%S")
                                time_bd_fim = datetime.strptime(str(fim),"%H:%M:%S")        

                                time_selec_inicio = datetime.strptime(str(opt_option_ini.get()),"%H:%M:%S")
                                time_selec_fim = datetime.strptime(str(opt_option_fim.get()),"%H:%M:%S")
                                confirma = True
                                if id != resultado[0]:
                                    if (time_selec_inicio >= time_bd_inicio and time_selec_inicio < time_bd_fim) or (time_selec_fim > time_bd_inicio and time_selec_fim <= time_bd_fim) or (time_selec_inicio < time_bd_inicio and time_selec_fim >= time_bd_fim):
                                        confirma = False
                                        break
                            if confirma == True:
                                confirmacao()
                            else:
                                messagebox.showwarning('Simec Agenda', 'Intervalo de horário indisponível.', parent=root)

                else:
                    confirmacao()

        def cancelar_editar():
            agendar()
        
        lista_select = tree_agenda.focus()

        if lista_select == "":
            messagebox.showwarning('Simec Agenda:', 'Selecione a reunião que deseja editar.', parent=root)
        else:
            valor_lista = tree_agenda.item(lista_select, "values")[0]
            cursor.execute("select * from agendas where id = %s",(valor_lista,))
            resultado = cursor.fetchone()

            usuario_bd = resultado[6]
            if usuario_bd != usuario_logado:
                messagebox.showwarning('Simec Agenda:', 'Não é permitido editar a reunião de outro usuário!', parent=root)
            else:
                db.cmd_reset_connection()
                tree_agenda.delete(*tree_agenda.get_children())    
                data = resultado[1]
                sala = resultado[5]
                cursor.execute("SELECT * FROM agendas where data = %s and sala = %s order by data, sala, hora_inicio",(data,sala,))
                cont = 0
                for row in cursor:
                    data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
                    if data_banco >= data_hoje:

                        if cont % 2 == 0:
                            tree_agenda.insert('', 'end', text=" ",
                                                    values=(
                                                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                                    tags=('par',))
                        else:
                            tree_agenda.insert('', 'end', text=" ",
                                                    values=(
                                                    row[0], row[1], row[2], row[3], row[4], row[5], row[6]),
                                                    tags=('impar',))
                        cont += 1

                setup_editar()
                bt_confirma.grid_remove()
                bt_editar.grid_remove()
                bt_cancela.grid_remove()
                
                bt_confirma_editar = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=confirma_edicao, width=100)
                bt_confirma_editar.grid(row=0, column=1, padx=10)
                bt_cancela_editar = customtkinter.CTkButton(fr8, text='Cancelar', **bt_cancela1, command=cancelar_editar, width=100)
                bt_cancela_editar.grid(row=0, column=3, padx=10)

    def login():
        if usuario_logado == '':
            def logar_bind(event):
                entrar()
            
            def entrar():
                user = ent_usuario.get()
                senha = ent_senha.get()
                if user == "" or senha == "":
                    messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root2)
                else:
                    server_name = '192.168.1.19'
                    domain_name = 'gvdobrasil'
                    server = Server(server_name, get_info=ALL)
                    try:
                        Connection(server, user='{}\\{}'.format(domain_name, user), password=senha, authentication=NTLM,
                                    auto_bind=True)
                    except:
                        messagebox.showwarning('Simec Agenda', 'Usuário ou senha inválidos.', parent=root2)
                        return False
                    global usuario_logado
                    usuario_logado = user
                    root2.destroy()
                    #print(usuario_logado)
            def cancelar_login():
                lista_contatos()
                root2.destroy()
                
            root2 = Toplevel(root)
            root2.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())
            root2.unbind_class("Button", "<Key-space>")
            root2.focus_force()
            root2.grab_set()

            window_width = 500
            window_height = 350
            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight() - 70
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            root2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
            root2.resizable(0, 0)
            root2.configure(bg='#ffffff')
            root2.title(titulos)
            root2.iconbitmap('img\\icone.ico')

            fr1 = Frame(root2, bg='#ffffff')
            fr1.pack(side=TOP, fill=X, expand=False)
            fr2 = Frame(root2, bg='#eeeeee') #/// LINHA
            fr2.pack(side=TOP, fill=X, expand=False, pady=10)
            fr3 = Frame(root2, bg='#ffffff')
            fr3.pack(side=TOP, fill=X, expand=False)
            fr4 = Frame(root2, bg='#eeeeee') #/// LINHA
            fr4.pack(side=TOP, fill=X, expand=False, pady=10)
            fr5 = Frame(root2, bg='#ffffff')
            fr5.pack(side=TOP, fill=X, expand=False, pady=5)
            fr6 = Frame(root2, bg='#1D366C')
            fr6.pack(side=BOTTOM, fill=X, expand=False)
            
            #// Frame1
            img_phone = Image.open('img\\chave.png')
            resize_phone = img_phone.resize((30, 30))
            nova_img_phone = ImageTk.PhotoImage(resize_phone)
            lbl_phone = Label(fr1, image=nova_img_phone, text=' Login', font=ft_titulo, compound='left', background=cor_branca, fg=cor_primaria)
            lbl_phone.photo = nova_img_phone
            lbl_phone.grid(row=0, column=0, padx=20)
            
            #// Frame2 Linha

            #// Frame3
            lbl = Label(fr3, text='Usuário', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
            lbl.grid(row=0, column=1, sticky=W)
            ent_usuario = customtkinter.CTkEntry(fr3, width=250, height=25, placeholder_text='Usuário do domínio', **ent_padrao_form) 
            ent_usuario.grid(row=1, column=1, pady=(0,10))       
            ent_usuario.bind("<Return>", logar_bind)

            lbl = Label(fr3, text='Senha', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
            lbl.grid(row=2, column=1, sticky=W)
            ent_senha = customtkinter.CTkEntry(fr3, width=250, height=25, show='*', placeholder_text='Senha do domínio', **ent_padrao_form) 
            ent_senha.grid(row=3, column=1, pady=(0,10))       
            ent_senha.bind("<Return>", logar_bind)
            
            fr3.grid_columnconfigure(0, weight=1) 
            fr3.grid_columnconfigure(3, weight=1) 
            
            #// Frame4 Linha
            
            #// Frame5
            bt_confirma = customtkinter.CTkButton(fr5, text='Confirmar', **bt_confirma1, command=entrar, width=100)
            bt_confirma.grid(row=0, column=1, padx=10)
            bt_cancela = customtkinter.CTkButton(fr5, text='Cancelar', **bt_cancela1, command=cancelar_login, width=100)
            bt_cancela.grid(row=0, column=2, padx=10)

            fr5.grid_columnconfigure(0, weight=1) 
            fr5.grid_columnconfigure(3, weight=1) 

            img_barra = Image.open('img\\logo_simec.png')
            resize_barra = img_barra.resize((90, 32))
            nova_img_barra = ImageTk.PhotoImage(resize_barra)
            lbl_barra = Label(fr6, image=nova_img_barra, background=cor_primaria, height=40)
            lbl_barra.photo = nova_img_barra
            lbl_barra.grid(row=0, column=1, padx=20)

            fr6.grid_columnconfigure(0, weight=1)
            fr6.grid_columnconfigure(3, weight=1)

            root2.wm_protocol("WM_DELETE_WINDOW", lambda: [lista_contatos(), root2.destroy()])
            root2.mainloop()
    
    #// Layout
    fr1 = Frame(frame4, bg='#ffffff')
    fr1.pack(side=TOP, fill=X, expand=False)
    fr2 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr2.pack(side=TOP, fill=X, expand=False, pady=10)
    fr3 = Frame(frame4, bg='#ffffff')
    fr3.pack(side=TOP, fill=X, expand=False)
    fr4 = Frame(frame4, bg='#ffffff')
    fr4.pack(side=TOP, fill=X, expand=False, pady=5)
    fr5 = Frame(frame4, bg='#ffffff')
    fr5.pack(side=TOP, fill=X, expand=False, pady=5)
    fr6 = Frame(frame4, bg='#ffffff')
    fr6.pack(side=TOP, fill=X, expand=False, pady=5)    
    fr7 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr7.pack(side=TOP, fill=X, expand=False, pady=10)
    fr8 = Frame(frame4, bg='#ffffff')
    fr8.pack(side=TOP, fill=X, expand=False)
    fr9 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr9.pack(side=TOP, fill=X, expand=False, pady=10)
    fr10 = Frame(frame4, bg='#ffffff')
    fr10.pack(side=TOP, fill=BOTH, expand=True)

    #// Frame1
    img_phone = Image.open('img\\agenda.png')
    resize_phone = img_phone.resize((30, 30))
    nova_img_phone = ImageTk.PhotoImage(resize_phone)
    lbl_phone = Label(fr1, image=nova_img_phone, text=' Agendar Reunião', font=ft_titulo, compound='left', background=cor_branca, fg=cor_primaria)
    lbl_phone.photo = nova_img_phone
    lbl_phone.grid(row=0, column=0, padx=20)

    clique_option = StringVar()
    lista_area = ['Data', 'Sala']
    opt_busca = customtkinter.CTkOptionMenu(fr1, variable=clique_option, values=lista_area, width=150, height=25, **opt_menu)
    opt_busca.grid(row=0, column=2, padx=0)
    opt_busca.set('Data')

    img_lupa = Image.open('img\\lupa.png')
    resize_lupa = img_lupa.resize((20, 20))
    nova_img_lupa = ImageTk.PhotoImage(resize_lupa)
    bt_lupa = Button(fr1, image=nova_img_lupa, **bt_icone, command=busca)
    bt_lupa.photo = nova_img_lupa
    bt_lupa.grid(row=0, column=3, padx=4)

    ent_busca = customtkinter.CTkEntry(fr1, width=150, height=25, placeholder_text='Procurar', **ent_padrao, textvariable=busca) 
    ent_busca.grid(row=0, column=4, padx=(0,20))       
    ent_busca.bind("<Return>", busca_bind)

    fr1.grid_columnconfigure(1, weight=1) 

    #// Frame2 Linha

    #// Frame3
    lbl = Label(fr3, text='Adicionar título', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W)
    ent_titulo = customtkinter.CTkEntry(fr3, width=400, height=25, placeholder_text='Adicionar título', **ent_padrao_form) 
    ent_titulo.grid(row=1, column=1, pady=(0,10))       

    fr3.grid_columnconfigure(0, weight=1) 
    fr3.grid_columnconfigure(2, weight=1) 

    #// Frame4
    lbl = Label(fr4, text='Escolha uma sala', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W)
    clique_sala = StringVar()
    lista_sala = [
        'Sala de Reunião Adm 1',
        'Sala de Reunião Adm 2',
        'Sala de Reunião Aciaria',
        'Sala de Reunião Laminação'
        ]
    opt_sala = customtkinter.CTkOptionMenu(fr4, variable=clique_sala, values=lista_sala, **opt_menu, width=250, height=25, command=filtro_escolha_sala)
    opt_sala.grid(row=0, column=2)
    
    fr4.grid_columnconfigure(0, weight=1) 
    fr4.grid_columnconfigure(3, weight=1) 
    
    #// Frame5
    img_data = Image.open('img\\agenda.png')
    resize_data = img_data.resize((25, 25))
    nova_img_data = ImageTk.PhotoImage(resize_data)
    lbl_data = Button(fr5, image=nova_img_data, text='Escolha uma data  ', font=ft_titulo, compound='righ', fg=cor_secundaria, **bt_icone, command=calendario)
    lbl_data.photo = nova_img_data
    lbl_data.grid(row=2, column=1, sticky=W)
    ent_data = customtkinter.CTkEntry(fr5, width=400, height=25, placeholder_text='Escolha uma data', **ent_padrao_form, state='readonly', ) 
    ent_data.grid(row=3, column=1)

    fr5.grid_columnconfigure(0, weight=1) 
    fr5.grid_columnconfigure(5, weight=1) 
    
    #// Frame6
    lbl = Label(fr6, text='Início', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W)
    clique_inicio = StringVar()
    lista_hora_inicio = [
        '07:00:00',
        '07:30:00',
        '08:00:00',
        '08:30:00',
        '09:00:00',
        '09:30:00',
        '10:00:00',
        '10:30:00',
        '11:00:00',
        '11:30:00',
        '12:00:00',
        '12:30:00',
        '13:00:00',
        '13:30:00',
        '14:00:00',
        '14:30:00',
        '15:00:00',
        '15:30:00',
        '16:00:00',
        '16:30:00',
        '17:00:00',
        '17:30:00',
        '18:00:00']
    
    opt_option_ini = ttk.Combobox(fr6, textvariable=clique_inicio, values=lista_hora_inicio, width=15, font=ft_padrao, state='readonly')
    opt_option_ini.grid(row=0, column=2)
    #opt_option_ini.set('11:00:00')

    lbl = Label(fr6, text='-', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=3, padx=10)

    lbl = Label(fr6, text='Fim', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=4, sticky=W)
    clique_fim = StringVar()
    opt_option_fim = ttk.Combobox(fr6, textvariable=clique_fim, values=lista_hora_inicio, width=15, font=ft_padrao, state='readonly')
    opt_option_fim.grid(row=0, column=5)
    #opt_option_fim.set('11:30:00')

    fr6.grid_columnconfigure(0, weight=1) 
    fr6.grid_columnconfigure(6, weight=1) 
    
    #// Frame7 Linha

    #// Frame8
    bt_confirma = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=salvar, width=100)
    bt_confirma.grid(row=0, column=1, padx=10)
    
    bt_editar = customtkinter.CTkButton(fr8, text='Editar', **bt_edita1, command=editar, width=100)
    bt_editar.grid(row=0, column=2, padx=10)    
    
    bt_cancela = customtkinter.CTkButton(fr8, text='Excluir', **bt_cancela1, command=excluir, width=100)
    bt_cancela.grid(row=0, column=3, padx=10)

    fr8.grid_columnconfigure(0, weight=1) 
    fr8.grid_columnconfigure(4, weight=1) 

    #// Frame9 Linha

    #// Frame10
    style = ttk.Style()
    #style.theme_use('default')
    style.configure('Treeview',
                    background=cor_branca,
                    rowheight=24,
                    fieldbackground=cor_branca,
                    font=ft_padrao)
    style.configure("Treeview.Heading",
                    foreground=cor_primaria,
                    background=cor_branca,
                    height=200,
                    font=ft_padrao)
    style.map('Treeview', background=[('selected', cor_primaria2)])

    tree_agenda = ttk.Treeview(fr10, selectmode='browse')
    vsb = ttk.Scrollbar(fr10, orient="vertical", command=tree_agenda.yview)
    vsb.pack(side=RIGHT, fill='y')
    tree_agenda.configure(yscrollcommand=vsb.set)
    vsbx = ttk.Scrollbar(fr10, orient="horizontal", command=tree_agenda.xview)
    vsbx.pack(side=BOTTOM, fill='x')
    tree_agenda.configure(xscrollcommand=vsbx.set)
    tree_agenda.pack(side=LEFT, fill=BOTH, expand=True, anchor='n')
    tree_agenda["columns"] = ("1", "2", "3", "4", "5", "6", "7")
    tree_agenda['show'] = 'headings'
    tree_agenda.column("1", anchor='c')
    tree_agenda.column("2", anchor='c')
    tree_agenda.column("3", anchor='c')
    tree_agenda.column("4", anchor='c')
    tree_agenda.column("5", anchor='c')    
    tree_agenda.column("6", anchor='c')        
    tree_agenda.column("7", anchor='c')        
    tree_agenda.heading("1", text="ID")
    tree_agenda.heading("2", text="Data")
    tree_agenda.heading("3", text="Título")
    tree_agenda.heading("4", text="Início")    
    tree_agenda.heading("5", text="Fim")
    tree_agenda.heading("6", text="Sala")
    tree_agenda.heading("7", text="Usuário")
    tree_agenda.tag_configure('par', background=cor_cfraca)
    tree_agenda.tag_configure('impar', background=cor_branca)
    atualiza_lista()
    login()

def agendar_motorista():
    for widget in frame4.winfo_children():
            widget.destroy()
    #// Funcoes
    def atualiza_lista():
        db.cmd_reset_connection()
        tree_agenda.delete(*tree_agenda.get_children())
        cursor.execute("SELECT * from agendas_motorista order by data, hora_inicio")
        cont = 0
        for row in cursor:
            data_banco = datetime.strptime(str(row[1]), "%d/%m/%Y")
            if data_banco >= data_hoje:
                if cont % 2 == 0:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                            tags=('par',))
                else:
                    tree_agenda.insert('', 'end', text=" ",
                                            values=(
                                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                            tags=('impar',))
                cont += 1

    def limpar_consulta(event):
        if opt_busca.get() == 'Limpar Consulta':
            atualiza_lista()
            opt_busca.set('Data')
            ent_busca.delete(0,END)

    def busca_bind(event):
        busca()
    
    def busca():
        opt = opt_busca.get()
        db.cmd_reset_connection()
        if opt == 'Data':
            busca = ent_busca.get()
            if busca == '':
                print('vazio')
            else:
                tree_agenda.delete(*tree_agenda.get_children())    
                query = "SELECT * FROM agendas_motorista where data LIKE '%"+busca+"%' order by data, hora_inicio, motorista"
                cursor.execute(query)
                
                cont = 0
                for row in cursor:
                    if cont % 2 == 0:
                        tree_agenda.insert('', 'end', text=" ",
                                                values=(
                                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                                tags=('par',))
                    else:
                        tree_agenda.insert('', 'end', text=" ",
                                                values=(
                                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                                tags=('impar',))
                    cont += 1

        elif opt == 'Motorista':
            busca = ent_busca.get()
            if busca == '':
                print('vazio')            
            else:
                tree_agenda.delete(*tree_agenda.get_children())    
                query = "SELECT * FROM agendas_motorista where motorista LIKE '%"+busca+"%' order by data, hora_inicio, motorista"
                cursor.execute(query)            
                cont = 0
                for row in cursor:
                    if cont % 2 == 0:
                        tree_agenda.insert('', 'end', text=" ",
                                                values=(
                                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                                tags=('par',))
                    else:
                        tree_agenda.insert('', 'end', text=" ",
                                                values=(
                                                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]),
                                                tags=('impar',))
                    cont += 1                

    def calendario():
        root2 = Toplevel(root)
        window_width = 360
        window_height = 258
        screen_width = root2.winfo_screenwidth()
        screen_height = root2.winfo_screenheight() - 70
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        root2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        root2.resizable(0, 0)
        root2.configure(bg='#ffffff')
        root2.title(titulos)
        root2.overrideredirect(True)
        root2.focus_force()
        root2.grab_set()

        def escolher_data_bind(event):
            escolher_data()
        def escolher_data():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.insert(0, cal.get_date())
            ent_data.configure(state='readonly')
            root2.destroy()
            root.focus_force()
            root.grab_set()
        
        hoje = date.today()
        cal = Calendar(root2, font=ft_padrao, selectmode='day', locale='pt_BR',
                   mindate=hoje, cursor="hand1", background=cor_primaria2, foreground=cor_branca, bordercolor=cor_primaria2, headersbackground=cor_cfraca, headersforeground=cor_secundaria )
        
        cal.pack(fill="both", expand=True)
    
        root2.bind('<Double-1>',escolher_data_bind) # Escolhe a data ao clicar 2x com o mouse
        root2,mainloop()

    def salvar():
        def limpar_campos():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.configure(state='readonly')

            opt_option_ini.set('')

            ent_solicitante.delete(0, END)
            
            ent_destino.delete(0, END)

            ent_motivo.delete(0, END)

            ent_obs.delete(0, END)

            ent_motorista.delete(0, END)

        data_agenda = ent_data.get()
        hora_inicio = clique_inicio.get()
        solicitante = ent_solicitante.get().upper()
        destino = ent_destino.get().upper()
        motivo = ent_motivo.get().upper()
        motorista = ent_motorista.get().upper()        
        obs = ent_obs.get().upper()        
        if data_agenda == '' or  hora_inicio == '' or solicitante == '' or destino == '' or motivo == '' or obs == '' or motorista == '':
            messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root)
        else:
            try:
                cursor.execute("INSERT INTO agendas_motorista (\
                    data,\
                    solicitante,\
                    destino,\
                    motivo,\
                    hora_inicio,\
                    motorista,\
                    obs)\
                    values(%s,%s,%s,%s,%s,%s,%s)", (data_agenda, solicitante, destino, motivo, hora_inicio, motorista, obs))
                db.commit()
            except:
                messagebox.showerror('Simec Agenda', 'Erro de conexão com o Banco de Dados.', parent=root)
                return False
            messagebox.showinfo('Simec Agenda', 'Viagem agendada com sucesso.', parent=root)
            atualiza_lista()
            limpar_campos()

    def excluir():
        def limpar_campos():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.configure(state='readonly')

            opt_option_ini.set('')

            ent_solicitante.delete(0, END)
            
            ent_destino.delete(0, END)

            ent_motivo.delete(0, END)

            ent_obs.delete(0, END)

            ent_motorista.delete(0, END)

        lista_select = tree_agenda.focus()
        if lista_select == "":
            messagebox.showwarning('Simec Agenda:', 'Selecione o item que deseja excluir.', parent=root)
        else:
            valor_lista = tree_agenda.item(lista_select, "values")[0]
            
            cursor.execute("select usuario from agendas where id = %s",(valor_lista,))
            resp = messagebox.askyesno('Simec Agenda:', 'Confirma a exclusão desta viagem?', parent=root)
            if resp:
                try:
                    cursor.execute("DELETE from agendas_motorista where id = %s",(valor_lista,))
                    db.commit()
                except:
                    messagebox.showerror('Simec Agenda:', 'Erro de conexão com o Banco de Dados.', parent=root)
                    return False
                messagebox.showinfo('Simec Agenda:', 'Viagem excluída com sucesso.', parent=root)
                atualiza_lista()
                limpar_campos()

    def editar():
        def setup_editar():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.insert(0, resultado[1])
            ent_data.configure(state='readonly')

            opt_option_ini.set(resultado[5])

            ent_solicitante.delete(0, END)
            ent_solicitante.insert(0, resultado[2])
            
            ent_destino.delete(0, END)
            ent_destino.insert(0, resultado[3])

            ent_motivo.delete(0, END)
            ent_motivo.insert(0, resultado[4])

            ent_obs.delete(0, END)
            ent_obs.insert(0, resultado[7])

            ent_motorista.delete(0, END)
            ent_motorista.insert(0, resultado[6])

        def confirma_edicao():
            def confirmacao():
                def limpar_campos():
                    ent_data.configure(state='normal')
                    ent_data.delete(0, END)
                    ent_data.configure(state='readonly')

                    opt_option_ini.set('')

                    ent_solicitante.delete(0, END)
                    
                    ent_destino.delete(0, END)

                    ent_motivo.delete(0, END)

                    ent_obs.delete(0, END)

                    ent_motorista.delete(0, END)

                    bt_confirma = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=salvar, width=100)
                    bt_confirma.grid(row=0, column=1, padx=10)
                    
                    bt_editar = customtkinter.CTkButton(fr8, text='Editar', **bt_edita1, command=editar, width=100)
                    bt_editar.grid(row=0, column=2, padx=10)    
                    
                    bt_cancela = customtkinter.CTkButton(fr8, text='Excluir', **bt_cancela1, command=excluir, width=100)
                    bt_cancela.grid(row=0, column=3, padx=10)

                try:
                    cursor.execute("UPDATE agendas_motorista SET\
                        data = %s,\
                        solicitante = %s,\
                        destino = %s,\
                        motivo = %s,\
                        hora_inicio = %s,\
                        motorista = %s,\
                        obs = %s\
                        WHERE id = %s", (data_agenda, solicitante, destino, motivo, hora_inicio, motorista, obs, resultado[0]))
                    db.commit()
                except:
                    messagebox.showerror('Simec Agenda:', 'Erro de conexão com o Banco de Dados.', parent=root)
                    return False
                messagebox.showinfo('Simec Agenda:', 'Viagem editada com sucesso.', parent=root)
                atualiza_lista()
                limpar_campos()

            data_agenda = ent_data.get()
            hora_inicio = clique_inicio.get()
            solicitante = ent_solicitante.get().upper()
            destino = ent_destino.get().upper()
            motivo = ent_motivo.get().upper()
            motorista = ent_motorista.get().upper()        
            obs = ent_obs.get().upper()        

            if data_agenda == '' or  hora_inicio == '' or solicitante == '' or destino == '' or motivo == '' or obs == '' or motorista == '':
                messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root)
            else:
                confirmacao()

        def cancelar_editar():
            ent_data.configure(state='normal')
            ent_data.delete(0, END)
            ent_data.configure(state='readonly')

            opt_option_ini.set('')

            ent_solicitante.delete(0, END)
            
            ent_destino.delete(0, END)

            ent_motivo.delete(0, END)

            ent_obs.delete(0, END)

            ent_motorista.delete(0, END)

            bt_confirma = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=salvar, width=100)
            bt_confirma.grid(row=0, column=1, padx=10)
            
            bt_editar = customtkinter.CTkButton(fr8, text='Editar', **bt_edita1, command=editar, width=100)
            bt_editar.grid(row=0, column=2, padx=10)    
            
            bt_cancela = customtkinter.CTkButton(fr8, text='Excluir', **bt_cancela1, command=excluir, width=100)
            bt_cancela.grid(row=0, column=3, padx=10)            

        
        lista_select = tree_agenda.focus()

        if lista_select == "":
            messagebox.showwarning('Simec Agenda:', 'Selecione o item que deseja editar.', parent=root)
        else:
            valor_lista = tree_agenda.item(lista_select, "values")[0]
            cursor.execute("select * from agendas_motorista where id = %s",(valor_lista,))
            resultado = cursor.fetchone()
            setup_editar()
            bt_confirma.grid_remove()
            bt_editar.grid_remove()
            bt_cancela.grid_remove()
           
            bt_confirma_editar = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=confirma_edicao, width=100)
            bt_confirma_editar.grid(row=0, column=1, padx=10)
            bt_cancela_editar = customtkinter.CTkButton(fr8, text='Cancelar', **bt_cancela1, command=cancelar_editar, width=100)
            bt_cancela_editar.grid(row=0, column=3, padx=10)

    def login():
        def estrutura_login():
            def logar_bind(event):
                entrar()
            
            def entrar():
                user = ent_usuario.get()
                senha = ent_senha.get()
                if user == "" or senha == "":
                    messagebox.showwarning('Simec Agenda', 'Todos os campos devem ser preenchidos.', parent=root2)
                else:
                    server_name = '192.168.1.19'
                    domain_name = 'gvdobrasil'
                    server = Server(server_name, get_info=ALL)
                    try:
                        Connection(server, user='{}\\{}'.format(domain_name, user), password=senha, authentication=NTLM,
                                    auto_bind=True)
                    except:
                        messagebox.showwarning('Simec Agenda', 'Usuário ou senha inválidos.', parent=root2)
                        return False
                    global usuario_logado
                    usuario_logado = user
                    cursor.execute('select usuario from usuarios_autorizados where usuario = %s',(usuario_logado,))
                    retorno = cursor.fetchone()
                    if retorno == None:
                        messagebox.showwarning('Simec Agenda', 'Usuário sem permissão para acessar este módulo.', parent=root2)
                    else:
                        root2.destroy()
                        atualiza_lista()

            def cancelar_login():
                lista_contatos()
                root2.destroy()
                
            root2 = Toplevel(root)
            root2.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())
            root2.unbind_class("Button", "<Key-space>")
            root2.focus_force()
            root2.grab_set()

            window_width = 500
            window_height = 350
            screen_width = root2.winfo_screenwidth()
            screen_height = root2.winfo_screenheight() - 70
            x_cordinate = int((screen_width / 2) - (window_width / 2))
            y_cordinate = int((screen_height / 2) - (window_height / 2))
            root2.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
            root2.resizable(0, 0)
            root2.configure(bg='#ffffff')
            root2.title(titulos)
            root2.iconbitmap('img\\icone.ico')

            fr1 = Frame(root2, bg='#ffffff')
            fr1.pack(side=TOP, fill=X, expand=False)
            fr2 = Frame(root2, bg='#eeeeee') #/// LINHA
            fr2.pack(side=TOP, fill=X, expand=False, pady=10)
            fr3 = Frame(root2, bg='#ffffff')
            fr3.pack(side=TOP, fill=X, expand=False)
            fr4 = Frame(root2, bg='#eeeeee') #/// LINHA
            fr4.pack(side=TOP, fill=X, expand=False, pady=10)
            fr5 = Frame(root2, bg='#ffffff')
            fr5.pack(side=TOP, fill=X, expand=False, pady=5)
            fr6 = Frame(root2, bg='#1D366C')
            fr6.pack(side=BOTTOM, fill=X, expand=False)
            
            #// Frame1
            img_phone = Image.open('img\\chave.png')
            resize_phone = img_phone.resize((30, 30))
            nova_img_phone = ImageTk.PhotoImage(resize_phone)
            lbl_phone = Label(fr1, image=nova_img_phone, text=' Login', font=ft_titulo, compound='left', background=cor_branca, fg=cor_primaria)
            lbl_phone.photo = nova_img_phone
            lbl_phone.grid(row=0, column=0, padx=20)
            
            #// Frame2 Linha

            #// Frame3
            lbl = Label(fr3, text='Usuário', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
            lbl.grid(row=0, column=1, sticky=W)
            ent_usuario = customtkinter.CTkEntry(fr3, width=250, height=25, placeholder_text='Usuário do domínio', **ent_padrao_form) 
            ent_usuario.grid(row=1, column=1, pady=(0,10))       
            ent_usuario.bind("<Return>", logar_bind)

            lbl = Label(fr3, text='Senha', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
            lbl.grid(row=2, column=1, sticky=W)
            ent_senha = customtkinter.CTkEntry(fr3, width=250, height=25, show='*', placeholder_text='Senha do domínio', **ent_padrao_form) 
            ent_senha.grid(row=3, column=1, pady=(0,10))       
            ent_senha.bind("<Return>", logar_bind)
            
            fr3.grid_columnconfigure(0, weight=1) 
            fr3.grid_columnconfigure(3, weight=1) 
            
            #// Frame4 Linha
            
            #// Frame5
            bt_confirma = customtkinter.CTkButton(fr5, text='Confirmar', **bt_confirma1, command=entrar, width=100)
            bt_confirma.grid(row=0, column=1, padx=10)
            bt_cancela = customtkinter.CTkButton(fr5, text='Cancelar', **bt_cancela1, command=cancelar_login, width=100)
            bt_cancela.grid(row=0, column=2, padx=10)

            fr5.grid_columnconfigure(0, weight=1) 
            fr5.grid_columnconfigure(3, weight=1) 

            img_barra = Image.open('img\\logo_simec.png')
            resize_barra = img_barra.resize((90, 32))
            nova_img_barra = ImageTk.PhotoImage(resize_barra)
            lbl_barra = Label(fr6, image=nova_img_barra, background=cor_primaria, height=40)
            lbl_barra.photo = nova_img_barra
            lbl_barra.grid(row=0, column=1, padx=20)

            fr6.grid_columnconfigure(0, weight=1)
            fr6.grid_columnconfigure(3, weight=1)

            root2.wm_protocol("WM_DELETE_WINDOW", lambda: [lista_contatos(), root2.destroy()])
            root2.mainloop()
        if usuario_logado == '':
            estrutura_login()
        else:
            cursor.execute('select usuario from usuarios_autorizados where usuario = %s',(usuario_logado,))
            retorno = cursor.fetchone()
            if retorno == None:
                estrutura_login()
            else:
                atualiza_lista()
    
    #// Layout
    fr1 = Frame(frame4, bg='#ffffff')
    fr1.pack(side=TOP, fill=X, expand=False)
    fr2 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr2.pack(side=TOP, fill=X, expand=False, pady=10)
    fr3 = Frame(frame4, bg='#ffffff')
    fr3.pack(side=TOP, fill=X, expand=False)
    fr4 = Frame(frame4, bg='#ffffff')
    fr4.pack(side=TOP, fill=X, expand=False, pady=5)
    fr5 = Frame(frame4, bg='#ffffff')
    fr5.pack(side=TOP, fill=X, expand=False, pady=5)
    fr6 = Frame(frame4, bg='#ffffff')
    fr6.pack(side=TOP, fill=X, expand=False, pady=5)    
    fr7 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr7.pack(side=TOP, fill=X, expand=False, pady=10)
    fr8 = Frame(frame4, bg='#ffffff')
    fr8.pack(side=TOP, fill=X, expand=False)
    fr9 = Frame(frame4, bg='#eeeeee') #/// LINHA
    fr9.pack(side=TOP, fill=X, expand=False, pady=10)
    fr10 = Frame(frame4, bg='#ffffff')
    fr10.pack(side=TOP, fill=BOTH, expand=True)

    #// Frame1
    img_phone = Image.open('img\\carros.png')
    resize_phone = img_phone.resize((35, 30))
    nova_img_phone = ImageTk.PhotoImage(resize_phone)
    lbl_phone = Label(fr1, image=nova_img_phone, text=' Agenda Motorista', font=ft_titulo, compound='left', background=cor_branca, fg=cor_primaria)
    lbl_phone.photo = nova_img_phone
    lbl_phone.grid(row=0, column=0, padx=20)

    clique_option = StringVar()
    lista_area = ['Data', 'Motorista', 'Limpar Consulta']
    opt_busca = customtkinter.CTkOptionMenu(fr1, variable=clique_option, values=lista_area, width=150, height=25, **opt_menu, command=limpar_consulta)
    opt_busca.grid(row=0, column=2, padx=0)
    opt_busca.set('Data')

    img_lupa = Image.open('img\\lupa.png')
    resize_lupa = img_lupa.resize((20, 20))
    nova_img_lupa = ImageTk.PhotoImage(resize_lupa)
    bt_lupa = Button(fr1, image=nova_img_lupa, **bt_icone, command=busca)
    bt_lupa.photo = nova_img_lupa
    bt_lupa.grid(row=0, column=3, padx=4)

    ent_busca = customtkinter.CTkEntry(fr1, width=150, height=25, placeholder_text='Procurar', **ent_padrao, textvariable=busca) 
    ent_busca.grid(row=0, column=4, padx=(0,20))       
    ent_busca.bind("<Return>", busca_bind)

    fr1.grid_columnconfigure(1, weight=1) 

    #// Frame2 Linha

    #// Frame3
    img_data = Image.open('img\\agenda.png')
    resize_data = img_data.resize((25, 25))
    nova_img_data = ImageTk.PhotoImage(resize_data)
    lbl_data = Button(fr3, image=nova_img_data, text='Escolha uma data  ', font=ft_titulo, compound='righ', fg=cor_secundaria, **bt_icone, command=calendario)
    lbl_data.photo = nova_img_data
    lbl_data.grid(row=0, column=1, sticky=W, padx=10)       
    ent_data = customtkinter.CTkEntry(fr3, width=300, height=25, placeholder_text='Escolha uma data', **ent_padrao_form, state='readonly', ) 
    ent_data.grid(row=1, column=1, padx=10)

    lbl = Label(fr3, text='Início', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=2, sticky=W, padx=10)
    clique_inicio = StringVar()
    lista_hora_inicio = [
        '00:00:00',
        '00:30:00',
        '01:00:00',
        '01:30:00',
        '02:00:00',
        '02:30:00',
        '03:00:00',
        '03:30:00',
        '04:00:00',
        '04:30:00',
        '05:00:00',
        '05:30:00',
        '06:00:00',
        '06:30:00',
        '07:00:00',
        '07:30:00',
        '08:00:00',
        '08:30:00',
        '09:00:00',
        '09:30:00',
        '10:00:00',
        '10:30:00',
        '11:00:00',
        '11:30:00',
        '12:00:00',
        '12:30:00',
        '13:00:00',
        '13:30:00',
        '14:00:00',
        '14:30:00',
        '15:00:00',
        '15:30:00',
        '16:00:00',
        '16:30:00',
        '17:00:00',
        '17:30:00',
        '18:00:00',
        '18:30:00',
        '19:00:00',
        '19:30:00',
        '20:00:00',
        '20:30:00',
        '21:00:00',
        '21:30:00',
        '22:00:00',
        '22:30:00',
        '23:00:00',
        '23:30:00']
   
    opt_option_ini = ttk.Combobox(fr3, textvariable=clique_inicio, values=lista_hora_inicio, width=34, font=ft_padrao, state='readonly')
    opt_option_ini.grid(row=1, column=2, padx=10)
    #opt_option_ini.set('11:00:00')    

    fr3.grid_columnconfigure(0, weight=1) 
    fr3.grid_columnconfigure(3, weight=1) 

    #// Frame4
    lbl = Label(fr4, text='Solicitante', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W, padx=10)       
    ent_solicitante = customtkinter.CTkEntry(fr4, width=300, height=25, placeholder_text='Solicitante', **ent_padrao_form) 
    ent_solicitante.grid(row=1, column=1, padx=10)       

    lbl = Label(fr4, text='Destino', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=2, sticky=W, padx=10)       
    ent_destino = customtkinter.CTkEntry(fr4, width=300, height=25, placeholder_text='Destino', **ent_padrao_form) 
    ent_destino.grid(row=1, column=2, padx=10)              

    fr4.grid_columnconfigure(0, weight=1) 
    fr4.grid_columnconfigure(3, weight=1) 

    
    #// Frame5
    lbl = Label(fr5, text='Motivo', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W, padx=10)       
    ent_motivo = customtkinter.CTkEntry(fr5, width=300, height=25, placeholder_text='Motivo', **ent_padrao_form) 
    ent_motivo.grid(row=1, column=1, padx=10)              

    lbl = Label(fr5, text='Observações', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=2, sticky=W, padx=10)       
    ent_obs = customtkinter.CTkEntry(fr5, width=300, height=25, placeholder_text='Observações', **ent_padrao_form) 
    ent_obs.grid(row=1, column=2, padx=10)              

    fr5.grid_columnconfigure(0, weight=1) 
    fr5.grid_columnconfigure(5, weight=1) 
    
    #// Frame6

    lbl = Label(fr6, text='Motorista', font=ft_titulo, background=cor_branca, fg=cor_secundaria)
    lbl.grid(row=0, column=1, sticky=W, padx=10)       
    ent_motorista = customtkinter.CTkEntry(fr6, width=300, height=25, placeholder_text='Motorista', **ent_padrao_form) 
    ent_motorista.grid(row=1, column=1, padx=10)              

    fr6.grid_columnconfigure(0, weight=1) 
    fr6.grid_columnconfigure(6, weight=1) 
    
    #// Frame7 Linha

    #// Frame8
    bt_confirma = customtkinter.CTkButton(fr8, text='Confirmar', **bt_confirma1, command=salvar, width=100)
    bt_confirma.grid(row=0, column=1, padx=10)
    
    bt_editar = customtkinter.CTkButton(fr8, text='Editar', **bt_edita1, command=editar, width=100)
    bt_editar.grid(row=0, column=2, padx=10)    
    
    bt_cancela = customtkinter.CTkButton(fr8, text='Excluir', **bt_cancela1, command=excluir, width=100)
    bt_cancela.grid(row=0, column=3, padx=10)

    fr8.grid_columnconfigure(0, weight=1) 
    fr8.grid_columnconfigure(4, weight=1) 

    #// Frame9 Linha

    #// Frame10
    style = ttk.Style()
    #style.theme_use('default')
    style.configure('Treeview',
                    background=cor_branca,
                    rowheight=24,
                    fieldbackground=cor_branca,
                    font=ft_padrao)
    style.configure("Treeview.Heading",
                    foreground=cor_primaria,
                    background=cor_branca,
                    height=200,
                    font=ft_padrao)
    style.map('Treeview', background=[('selected', cor_primaria2)])

    tree_agenda = ttk.Treeview(fr10, selectmode='browse')
    vsb = ttk.Scrollbar(fr10, orient="vertical", command=tree_agenda.yview)
    vsb.pack(side=RIGHT, fill='y')
    tree_agenda.configure(yscrollcommand=vsb.set)
    vsbx = ttk.Scrollbar(fr10, orient="horizontal", command=tree_agenda.xview)
    vsbx.pack(side=BOTTOM, fill='x')
    tree_agenda.configure(xscrollcommand=vsbx.set)
    tree_agenda.pack(side=LEFT, fill=BOTH, expand=True, anchor='n')
    tree_agenda["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
    tree_agenda['show'] = 'headings'
    tree_agenda.column("1", anchor='c')
    tree_agenda.column("2", anchor='c')
    tree_agenda.column("3", anchor='c')
    tree_agenda.column("4", anchor='c')
    tree_agenda.column("5", anchor='c')    
    tree_agenda.column("6", anchor='c')        
    tree_agenda.column("7", anchor='c')        
    tree_agenda.column("8", anchor='c')        
    tree_agenda.heading("1", text="ID")
    tree_agenda.heading("2", text="Data")
    tree_agenda.heading("3", text="Solicitante")
    tree_agenda.heading("4", text="Destino")    
    tree_agenda.heading("5", text="Motivo")
    tree_agenda.heading("6", text="Início")
    tree_agenda.heading("7", text="Motorista")
    tree_agenda.heading("8", text="Obs")    
    tree_agenda.tag_configure('par', background=cor_cfraca)
    tree_agenda.tag_configure('impar', background=cor_branca)
    login()
    
def verifica_versao():
    cursor.execute("SELECT versao FROM versao")
    versao = cursor.fetchone()
    if versao[0] != titulos:
        messagebox.showerror('Atualização:', f'Software desatualizado.\nVersão atual: "{versao[0]}". \n\nAtualize a versão de seu software.', parent=root)
        root.destroy()
    else:
        lista_contatos()
#// Root Config
root = customtkinter.CTk()
root.state('zoomed')
root.title(titulos)
root.iconbitmap('img\\icone.ico')
root.configure(background='#EEEEEE')
root.after(0,verifica_versao)

#// TTK Style
style = ttk.Style()
style.theme_use('clam')
style.theme_settings('clam', {
    'TCombobox':{
        'configure' : {
            'padding' : 4,
            'arrowcolor' : cor_secundaria,
            'arrowsize' : 15,
        }
    },
    'Vertical.TScrollbar' : {
        'configure' : {
            'background' : '#dedede',
            'troughcolor' : '#f1f1f1',
            'bordercolor' : '#dedede',
            'arrowcolor' : cor_secundaria,
            'lightcolor' : '#dedede',
            'arrowsize' : 15,
        }
    },
    'Horizontal.TScrollbar' : {
        'configure' : {
            'background' : '#dedede',
            'troughcolor' : '#f1f1f1',
            'bordercolor' : '#dedede',
            'arrowcolor' : cor_secundaria,
            'lightcolor' : '#dedede',
            'arrowsize' : 15,
        }
    },
    'Treeview' : {
        'configure' : {
            'background' : '#ffffff',
            'rowheight' : 24,
            'fieldbackground' : '#ffffff',
            'font' : ft_padrao,
        }
    },
    'Treeview.Heading' : {
        'configure' : {
            'background' : '#ffffff',
            'foreground' : '#1d366c',
            'font' : ft_padrao_bold,
            'borderwidth' : 0,
            'relief' : 'flat',
        }
    },
    })
root.option_add('*TCombobox*Listbox.background', cor_faded)
root.option_add('*TCombobox*Listbox.foreground', cor_secundaria)
root.option_add('*TCombobox*Listbox.selectBackground', cor_primaria2)
root.option_add('*TCombobox*Listbox.selectForeground', cor_branca)

style.map('Treeview', background=[('selected', cor_cfraca)])
style.map('Treeview.Heading', background=[('active', '#ffffff')])

style.map('TCombobox', background=[('readonly',cor_cfraca)])
style.map('TCombobox', fieldbackground=[('readonly',cor_cfraca)])
style.map('TCombobox', selectbackground=[('readonly', cor_cfraca)])
style.map('TCombobox', selectforeground=[('readonly', cor_secundaria)])
style.map('TCombobox', foreground=[('readonly', cor_secundaria)])

#//Layout
frame1 = Frame(root, bg=cor_primaria)
frame1.pack(padx=0, pady=0, fill=X, expand=False, side=TOP)

frame2 = Frame(root, bg=cor_primaria)
frame2.pack(padx=0, pady=0, fill=X, expand=False, side=BOTTOM)

frame3 = Frame(root, bg='#ffffff')
frame3.pack(padx=0, pady=0, fill=Y, expand=False, side=LEFT)
fr1 = Frame(frame3, bg=cor_branca)
fr1.pack(padx=0, pady=0, fill=X, expand=False, side=TOP)
fr2 = Frame(frame3, bg='#EEEEEE') #//Linha
fr2.pack(padx=0, pady=10, fill=X, expand=False, side=TOP)
fr3 = Frame(frame3, bg=cor_branca)
fr3.pack(padx=0, pady=0, fill=X, expand=False, side=TOP)
fr4 = Frame(frame3, bg='#EEEEEE') #//Linha
fr4.pack(padx=0, pady=10, fill=X, expand=False, side=TOP)
fr5 = Frame(frame3, bg=cor_branca)
fr5.pack(padx=0, pady=0, fill=X, expand=False, side=TOP)
fr6 = Frame(frame3, bg='#EEEEEE') #//Linha
fr6.pack(padx=0, pady=10, fill=X, expand=False, side=TOP)
fr7 = Frame(frame3, bg=cor_branca)
fr7.pack(padx=0, pady=0, fill=X, expand=False, side=TOP)


frame4 = customtkinter.CTkFrame (root, fg_color=cor_branca, )
frame4.pack(padx=20, pady=10, fill=BOTH, expand=True, side=LEFT)

#//Frame1
img_cont = Image.open('img\\logo.png')
resize_cont = img_cont.resize((40, 40))
nova_img_cont = ImageTk.PhotoImage(resize_cont)
lbl_cont = Label(frame1, image=nova_img_cont, text=' Simec Agenda', font=ft_titulo, compound='left', background=cor_primaria, fg=cor_branca)
lbl_cont.photo = nova_img_cont
lbl_cont.grid(row=0, column=0, padx=20)

img_sair = Image.open('img\\sair.png')
resize_sair = img_sair.resize((20, 20))
nova_img_sair = ImageTk.PhotoImage(resize_sair)
lbl_sair = Button(frame1, image=nova_img_sair, text=' Sair', font=ft_padrao, compound='left', background=cor_primaria, fg=cor_branca, borderwidth=0, highlightthickness=0, relief=RIDGE, activebackground=cor_primaria, activeforeground=cor_primaria, cursor='hand2', command=sair)
lbl_sair.photo = nova_img_sair
lbl_sair.grid(row=0, column=2, padx=20)

frame1.grid_columnconfigure(1, weight=1)

#//Frame2 Bottom
img_logo = Image.open('img\\logo_simec.png')
resize_logo = img_logo.resize((90, 32))
nova_img_logo = ImageTk.PhotoImage(resize_logo)
lbl_logo = Label(frame2, image=nova_img_logo, background=cor_primaria, height=40)
lbl_logo.photo = nova_img_logo
lbl_logo.grid(row=0, column=1, padx=20)

frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(3, weight=1)

#//Frame3 Menu Esquerda
img_bt1 = Image.open('img\\phone.png')
resize_bt1 = img_bt1.resize((30, 30))
nova_img_bt1 = ImageTk.PhotoImage(resize_bt1)
bt1 = customtkinter.CTkButton(fr3, image=nova_img_bt1 ,text='   Lista de Contatos', **bt_padrao, width=250, command=lista_contatos)
bt1.grid(row=0, column=1)

fr3.grid_columnconfigure(0, weight=1)
fr3.grid_columnconfigure(3, weight=1)

img_bt2 = Image.open('img\\agenda.png')
resize_bt2 = img_bt2.resize((30, 30))
nova_img_bt2 = ImageTk.PhotoImage(resize_bt2)
bt2 = customtkinter.CTkButton(fr5, image=nova_img_bt2 ,text='   Agendar Reunião', **bt_padrao, width=250, command=agendar)
bt2.grid(row=0, column=1)

img_bt3 = Image.open('img\\carros.png')
resize_bt3 = img_bt3.resize((30, 25))
nova_img_bt3 = ImageTk.PhotoImage(resize_bt3)
bt3 = customtkinter.CTkButton(fr7, image=nova_img_bt3 ,text='   Agenda Motorista', **bt_padrao, width=250, command=agendar_motorista)
bt3.grid(row=1, column=1)

#//Frame4 Conteudo

#// Conexao
db = mysql.connector.connect(
    #host="localhost",
    host="192.168.1.16",
    #user="root",
    user="acesso_rede",
    passwd="senha",
    database="simec_agenda",
)
cursor = db.cursor(buffered=True)

root.mainloop()
