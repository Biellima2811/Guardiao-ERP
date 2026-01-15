import ttkbootstrap as ttk
from core.security import SecurityAuth
from gui.screen_login import LoginScreen
# Importaremos o dashboard na próxima fase, por enquanto faremos um placeholder

class GuardiaoApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Guardião ERP - Login")
        self.geometry("1024x768")
        
        # 1. Inicializa Segurança (Cria admin se não existir)
        SecurityAuth.criar_admin_padrao()

        # 2. Mostra Login
        self.mostrar_login()

    def mostrar_login(self):
        self.login = LoginScreen(self, on_login_success=self.iniciar_sistema)

    def iniciar_sistema(self):
        self.title("Guardião ERP - Logado como Admin")
        # Aqui carregaremos a tela principal (Sidebar, Dashboard) que fizemos antes
        # Por enquanto, um aviso simples
        ttk.Label(self, text="BEM VINDO AO SISTEMA BLINDADO", font=("Calibri", 30)).pack(pady=50)
        ttk.Button(self, text="Sair", command=self.destroy).pack()

if __name__ == "__main__":
    app = GuardiaoApp()
    app.mainloop()