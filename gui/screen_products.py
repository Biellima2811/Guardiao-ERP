import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from core.product_model import ProductModel
from gui.popups import AddProductPopup

class ProductsScreen(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)
        self.pack(fill=BOTH, expand=YES)

        # Cabeçalho
        topo = ttk.Frame(self)
        topo.pack(fill=X, pady=(0, 20))
        ttk.Label(topo, text='Gestão de Estoque & Produtos', font=('Calibri', 24, 'bold'), bootstyle='primary').pack(side=LEFT)
        ttk.Button(topo, text='+ Novo Produto', bootstyle='success', command=self.abrir_popup_novo).pack(side=RIGHT)

        # Tabela
        colunas = ["id", "nome", "codigo", "estoque", "venda", "lucro"]
        self.tree = ttk.Treeview(self, columns=colunas, show='headings', bootstyle='primary')
        
        self.tree.column('id', width=50, anchor=CENTER)
        self.tree.column('nome', width=300, anchor=W)
        self.tree.column('codigo', width=100, anchor=CENTER)
        self.tree.column('estoque', width=80, anchor=CENTER)
        self.tree.column('venda', width=100, anchor=E)
        self.tree.column('lucro', width=100, anchor=E)
        
        self.tree.heading('id', text="ID")
        self.tree.heading('nome', text="Produto / Peça")
        self.tree.heading('codigo', text="Cód. Ref.")
        self.tree.heading('estoque', text="Qtd.")
        self.tree.heading('venda', text="Preço Venda")
        self.tree.heading('lucro', text="Lucro Est.")
        
        self.tree.pack(fill=BOTH, expand=YES)
        
        # Botões de Ação
        btn_frame = ttk.Frame(self, padding=(0, 10))
        btn_frame.pack(fill=X)
        
        ttk.Button(btn_frame, text="✏️ Editar Produto", bootstyle="warning", command=self.editar).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Excluir", bootstyle="danger", command=self.excluir).pack(side=LEFT, padx=5)

        self.carregar_dados()

    def carregar_dados(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        produtos = ProductModel.buscar_todos()
        for p in produtos:
            # p = (id, nome, codigo, estoque, venda, custo)
            venda_fmt = f"R$ {p[4]:.2f}"
            
            # Cálculo de Lucro
            custo = p[5] if p[5] else 0
            venda = p[4] if p[4] else 0
            lucro = venda - custo
            lucro_fmt = f"R$ {lucro:.2f}"
            
            self.tree.insert("", END, values=(p[0], p[1], p[2], p[3], venda_fmt, lucro_fmt))

    def abrir_popup_novo(self):
        AddProductPopup(self, on_confirm=self.carregar_dados)

    def editar(self):
        sel = self.tree.selection()
        if not sel: 
            # AQUI ESTAVA O ERRO SILENCIOSO: Faltava avisar!
            Messagebox.show_warning("Selecione um produto na tabela para editar.", "Atenção")
            return
        
        id_prod = self.tree.item(sel[0])['values'][0]
        dados = ProductModel.buscar_por_id(id_prod)
        AddProductPopup(self, on_confirm=self.carregar_dados, dados_edicao=dados)

    def excluir(self):
        sel = self.tree.selection()
        if not sel: 
            # AQUI TAMBÉM: Aviso adicionado
            Messagebox.show_warning("Selecione um produto para excluir.", "Atenção")
            return
            
        id_prod = self.tree.item(sel[0])['values'][0]
        
        if Messagebox.show_question("Excluir este produto do estoque?", "Confirmação") == "Yes":
            ProductModel.excluir(id_prod)
            self.carregar_dados()