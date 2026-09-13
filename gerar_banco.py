import sqlite3

# Cria o arquivo de banco de dados na mesma pasta
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Cria a estrutura das tabelas exigidas pelo professor
cursor.executescript('''
CREATE TABLE livros (
    isbn TEXT PRIMARY KEY,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    categoria TEXT,
    exemplares_disponiveis INTEGER DEFAULT 0
);

CREATE TABLE leitores (
    cpf TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT
);

CREATE TABLE emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_isbn TEXT NOT NULL,
    leitor_cpf TEXT NOT NULL,
    data_emprestimo TEXT NOT NULL,
    data_devolucao_prevista TEXT NOT NULL,
    data_devolucao TEXT,
    FOREIGN KEY (livro_isbn) REFERENCES livros(isbn),
    FOREIGN KEY (leitor_cpf) REFERENCES leitores(cpf)
);

CREATE TABLE multas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emprestimo_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    paga INTEGER DEFAULT 0,
    FOREIGN KEY (emprestimo_id) REFERENCES emprestimos(id)
);

CREATE TABLE reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_isbn TEXT NOT NULL,
    leitor_cpf TEXT NOT NULL,
    data_reserva TEXT NOT NULL,
    FOREIGN KEY (livro_isbn) REFERENCES livros(isbn),
    FOREIGN KEY (leitor_cpf) REFERENCES leitores(cpf)
);
''')

# Insere os dados de exemplo que estavam no arquivo original
cursor.executescript('''
INSERT INTO livros (isbn, titulo, autor, categoria, exemplares_disponiveis) VALUES 
('978-0321349606', 'Java Concurrency in Practice', 'Brian Goetz', 'Programação', 3),
('978-0132350884', 'Clean Code', 'Robert Martin', 'Programação', 5),
('978-0135957059', 'The Pragmatic Programmer', 'David Thomas', 'Programação', 2),
('978-0134685991', 'Effective Java', 'Joshua Bloch', 'Programação', 4);

INSERT INTO leitores (cpf, nome, email, telefone) VALUES 
('45678912300', 'Pedro Oliveira', 'pedro.oliveira@email.com', '11765432109'),
('98765432100', 'Maria Santos', 'maria.santos@email.com', '11876543210'),
('12345678901', 'João Silva', 'joao.silva@email.com', '11987654321');
''')

conn.commit()
conn.close()
print("O arquivo biblioteca.db foi criado com sucesso e está pronto para uso!")