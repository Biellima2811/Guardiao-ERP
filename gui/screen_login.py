import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core.security import SecurityAuth
from tkinter import messagebox

class LoginScreen(ttk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.pack(fill=BOTH, expand=YES)
        self.on_login_success = on_login_success

        # Layout Centralizado
        # CORREÇÃO: Nome da variável padronizado para frame_login
        self.frame_login = ttk.Frame(self, padding=40, bootstyle='secondary')
        self.frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Logo / Título
        ttk.Label(self.frame_login, text="GUARDIÃO ERP", 
                  font=("Calibri", 24, "bold"), 
                  bootstyle="inverse-secondary").pack(pady=(0, 20))
        
        ttk.Label(self.frame_login, 
                  text="Acesso Restrito", 
                  bootstyle="inverse-secondary").pack(pady=(0, 20))
        
        # Container para os campos (Grid dentro do Frame)
        grid_frame = ttk.Frame(self.frame_login, bootstyle="secondary")
        grid_frame.pack()

        # Campos
        ttk.Label(grid_frame, text='Usuário:', bootstyle='inverse-secondary').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.entry_user = ttk.Entry(grid_frame, width=30)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)
        self.entry_user.focus()

        ttk.Label(grid_frame, text='Senha:', bootstyle='inverse-secondary').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.entry_pass = ttk.Entry(grid_frame, width=30, show='*')
        self.entry_pass.grid(row=1, column=1, padx=5, pady=5)
        
        # CORREÇÃO: <Return> estava escrito errado
        self.entry_pass.bind('<Return>', lambda e: self.fazer_login())

        # Botão
        btn_entrar = ttk.Button(self.frame_login, text="ACESSAR SISTEMA", bootstyle="success", command=self.fazer_login)
        btn_entrar.pack(pady=20, fill=X)
        
        ttk.Label(self.frame_login, text="v1.0 Secure", font=("Arial", 8), bootstyle="inverse-secondary").pack()

    # CORREÇÃO: O método deve estar no nível da classe, não dentro do __init__
    def fazer_login(self):
        user = self.entry_user.get()
        senha = self.entry_pass.get()

        if SecurityAuth.login(user, senha):
            self.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Erro de Acesso", "Usuário ou senha inválidos!")