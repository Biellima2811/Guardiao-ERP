import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from core.dashboard_model import DashboardModel 

class DashboardScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        ttk.Label(self, text='Visão Geral', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(anchor=W, pady=(0,20))
        
        # --- CARDS DE KPI ---
        cards_frame = ttk.Frame(self)
        cards_frame.pack(fill=X, pady=10)

        total_clientes = DashboardModel.get_total_clientes()
        os_pendentes = DashboardModel.get_os_pendentes()
        faturamento = DashboardModel.get_faturamento_total()
        fat_formatado = f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        self.criar_card(cards_frame, 'Faturamento (Real)', fat_formatado, 'success', 0)
        self.criar_card(cards_frame, 'OS em Aberto', str(os_pendentes), 'warning', 1)
        self.criar_card(cards_frame, 'Clientes', str(total_clientes), 'info', 2)
        
        # --- SEÇÃO DE GRÁFICOS (METERS) ---
        graficos_frame = ttk.Labelframe(self, text="Performance & Metas", padding=15, bootstyle="secondary")
        graficos_frame.pack(fill=X, pady=20)

        # Dados para os gráficos
        taxa = DashboardModel.get_taxa_conclusao()
        progresso_meta = DashboardModel.get_progresso_meta(meta_mensal=10000) # Meta de R$ 10k

        # Gráfico 1: Taxa de Conclusão (Azul)
        meter1 = ttk.Meter(
            graficos_frame,
            metersize=160,
            padding=5,
            amountused=taxa,
            metertype="full",
            subtext="Taxa Conclusão",
            interactive=False,
            bootstyle="primary",
            textright="%"
        )
        meter1.pack(side=LEFT, padx=30)

        # Gráfico 2: Meta Financeira (Verde)
        meter2 = ttk.Meter(
            graficos_frame,
            metersize=160,
            padding=5,
            amountused=progresso_meta,
            metertype="semi", # Meia lua
            subtext="Meta R$ 10k",
            interactive=False,
            bootstyle="success",
            textright="%"
        )
        meter2.pack(side=LEFT, padx=30)

        # Texto de Apoio
        info_frame = ttk.Frame(graficos_frame)
        info_frame.pack(side=LEFT, padx=20, fill=Y)
        ttk.Label(info_frame, text="💡 Dica de Gestão:", font=("Calibri", 12, "bold")).pack(anchor=W)
        ttk.Label(info_frame, text="Mantenha a taxa de conclusão acima de 80% para\ngarantir a satisfação dos clientes e fluxo de caixa.", font=("Calibri", 10)).pack(anchor=W)

        # --- TABELA ---
        ttk.Label(self, text='Últimas Movimentações', font=('Calibri', 14, 'bold'), bootstyle="secondary").pack(anchor=W, pady=(20,10))
        
        colunas = ['Data', 'Cliente', 'Equipamento', 'Valor', 'Status']
        self.tree = ttk.Treeview(self, columns=colunas, show='headings', height=6, bootstyle='info')

        self.tree.column('Data', width=100, anchor=CENTER)
        self.tree.column('Cliente', width=300, anchor=W)
        self.tree.column('Equipamento', width=200, anchor=W)
        self.tree.column('Valor', width=100, anchor=E)
        self.tree.column('Status', width=120, anchor=CENTER)

        for col in colunas:
            self.tree.heading(col, text=col)
        
        self.tree.pack(fill=X)
        self.carregar_ultimas_os()
    
    def criar_card(self, parent, titulo, valor, cor, col):
        card = ttk.Frame(parent, bootstyle=cor, padding=15)
        card.pack(side=LEFT, fill=BOTH, expand=YES, padx=5)
        ttk.Label(card, text=titulo, font=("Calibri", 12), bootstyle=f"inverse-{cor}").pack(anchor=W)
        ttk.Label(card, text=valor, font=("Calibri", 22, "bold"), bootstyle=f"inverse-{cor}").pack(anchor=W)

    def carregar_ultimas_os(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        atividades = DashboardModel.get_ultimas_atividades()
        for item in atividades:
            data_fmt = item[0].split()[0] if item[0] else ""
            valor_fmt = f"R$ {item[3]:.2f}"
            self.tree.insert('', END, values=(data_fmt, item[1], item[2], valor_fmt, item[4]))