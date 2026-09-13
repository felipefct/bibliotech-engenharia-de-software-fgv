import sqlite3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from reportlab.pdfgen import canvas
from abc import ABC, abstractmethod

# ==========================================
# INTERFACES E REPOSITÓRIOS (Persistência)
# ==========================================
class IRepositorio(ABC):
    """Interface para operações de persistência"""
    @abstractmethod
    def buscar(self, id):
        pass
    
    @abstractmethod
    def salvar(self, entidade):
        pass

class RepositorioBase(IRepositorio):
    def __init__(self, db_path='../biblioteca.db'):
        self.db_path = db_path

    def _conectar(self):
        return sqlite3.connect(self.db_path)

class RepositorioLivro(RepositorioBase):
    def buscar(self, isbn):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM livros WHERE isbn = ?", (isbn,))
            return cursor.fetchone()
    
    def salvar(self, entidade):
        pass # Não utilizado neste fluxo específico
        
    def diminuir_estoque(self, isbn):
        with self._conectar() as conn:
            conn.execute("UPDATE livros SET exemplares_disponiveis = exemplares_disponiveis - 1 WHERE isbn = ?", (isbn,))
            conn.commit()

class RepositorioLeitor(RepositorioBase):
    def buscar(self, cpf):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM leitores WHERE cpf = ?", (cpf,))
            return cursor.fetchone()
            
    def salvar(self, entidade):
        pass

class RepositorioEmprestimo(RepositorioBase):
    def buscar(self, id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM emprestimos WHERE id = ?", (id,))
            return cursor.fetchone()

    def salvar(self, entidade):
        # entidade = (livro_isbn, leitor_cpf, data_emprestimo, data_devolucao_prevista)
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO emprestimos (livro_isbn, leitor_cpf, data_emprestimo, data_devolucao_prevista)
                VALUES (?, ?, ?, ?)
            """, entidade)
            conn.commit()
            return cursor.lastrowid
            
    def criar_reserva(self, isbn, cpf, data_reserva):
        with self._conectar() as conn:
            conn.execute("""
                INSERT INTO reservas (livro_isbn, leitor_cpf, data_reserva)
                VALUES (?, ?, ?)
            """, (isbn, cpf, data_reserva))
            conn.commit()
            
    def salvar_multa(self, emprestimo_id, valor):
        with self._conectar() as conn:
            conn.execute("INSERT INTO multas (emprestimo_id, valor) VALUES (?, ?)", (emprestimo_id, valor))
            conn.commit()

# ==========================================
# SERVIÇOS (Infraestrutura)
# ==========================================
class ServicoNotificacao:
    """Responsável apenas por enviar notificações"""
    def enviar_email(self, destinatario, assunto, mensagem):
        try:
            msg = MIMEText(mensagem)
            msg['Subject'] = assunto
            msg['To'] = destinatario
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('biblioteca@exemplo.com', 'senha')
            server.send_message(msg)
            server.quit()
        except Exception:
            pass # Ignora falhas de rede no ambiente de teste

class ServicoRelatorio:
    """Responsável apenas por gerar relatórios"""
    def gerar_comprovante_emprestimo(self, emprestimo_id, titulo_livro, nome_leitor, data_devolucao):
        try:
            c = canvas.Canvas(f'comprovante_{emprestimo_id}.pdf')
            c.drawString(100, 750, f'Empréstimo #{emprestimo_id}')
            c.drawString(100, 730, f'Livro: {titulo_livro}')
            c.drawString(100, 710, f'Leitor: {nome_leitor}')
            c.drawString(100, 690, f'Devolução: {data_devolucao}')
            c.save()
        except Exception:
            pass

class CalculadoraMulta:
    """Responsável apenas por calcular multas"""
    def __init__(self, taxa_diaria=2.0):
        self.taxa_diaria = taxa_diaria
        
    def calcular(self, data_prevista, data_atual=None):
        if data_atual is None:
            data_atual = datetime.now()
        data_prevista_obj = datetime.strptime(data_prevista, '%Y-%m-%d')
        
        if data_atual > data_prevista_obj:
            dias_atraso = (data_atual - data_prevista_obj).days
            return dias_atraso * self.taxa_diaria
        return 0.0

# ==========================================
# CLASSE PRINCIPAL (Regra de Negócio Orquestrada)
# ==========================================
class GerenciadorEmprestimo:
    """Orquestra o processo de empréstimo usando os serviços"""
    def __init__(
        self, 
        repo_livro: RepositorioLivro,
        repo_leitor: RepositorioLeitor,
        repo_emprestimo: RepositorioEmprestimo,
        servico_notificacao: ServicoNotificacao,
        servico_relatorio: ServicoRelatorio,
        calculadora_multa: CalculadoraMulta
    ):
        self.repo_livro = repo_livro
        self.repo_leitor = repo_leitor
        self.repo_emprestimo = repo_emprestimo
        self.servico_notificacao = servico_notificacao
        self.servico_relatorio = servico_relatorio
        self.calculadora_multa = calculadora_multa
    
    def realizar_emprestimo(self, livro_isbn: str, leitor_cpf: str) -> tuple:
        """Realiza empréstimo aplicando regras de negócio"""
        livro = self.repo_livro.buscar(livro_isbn)
        if not livro:
            return False, "Livro não encontrado"
            
        leitor = self.repo_leitor.buscar(leitor_cpf)
        if not leitor:
            return False, "Leitor não encontrado"
            
        exemplares_disponiveis = livro[4]
        
        if exemplares_disponiveis > 0:
            data_emprestimo = datetime.now().strftime('%Y-%m-%d')
            data_devolucao = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
            
            # Registra no BD
            entidade_emprestimo = (livro_isbn, leitor_cpf, data_emprestimo, data_devolucao)
            emprestimo_id = self.repo_emprestimo.salvar(entidade_emprestimo)
            self.repo_livro.diminuir_estoque(livro_isbn)
            
            # Infraestrutura acionada sem acoplamento direto
            self.servico_notificacao.enviar_email(leitor[2], 'Empréstimo Realizado', f"Empréstimo realizado: {livro[1]}")
            self.servico_relatorio.gerar_comprovante_emprestimo(emprestimo_id, livro[1], leitor[1], data_devolucao)
            
            return True, "Empréstimo realizado com sucesso"
        else:
            data_reserva = datetime.now().strftime('%Y-%m-%d')
            self.repo_emprestimo.criar_reserva(livro_isbn, leitor_cpf, data_reserva)
            return False, "Livro indisponível. Reserva criada."