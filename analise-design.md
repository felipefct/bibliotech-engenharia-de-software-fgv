# Questão 3: Princípios de Design e SOLID

## Análise do código original (gerenciador_original.py)

**1. Violações de Princípios SOLID identificadas:**
*   **SRP (Princípio da Responsabilidade Única):** A classe `GerenciadorEmprestimo` está acumulando múltiplas responsabilidades. Ela lida com a conexão ao banco de dados SQLite, envia e-mails usando `smtplib`, gera PDFs com `reportlab` e aplica as regras de negócio de datas e multas. 
*   **OCP (Princípio do Aberto/Fechado):** A classe não está fechada para modificações. Se precisarmos mudar o método de notificação de e-mail para SMS, ou o banco de dados de SQLite para PostgreSQL, o código fonte de `GerenciadorEmprestimo` terá que ser alterado.
*   **DIP (Princípio da Inversão de Dependência):** A classe principal de alto nível depende de implementações concretas (módulos de e-mail, PDF, SQLite) em vez de depender de abstrações (interfaces de serviços ou repositórios).

**2. Problemas de Coesão e Acoplamento:**
*   **Baixa Coesão:** Os métodos são muito grandes e lidam com operações que não se relacionam diretamente entre si na mesma abstração (ex: misturar lógica de SQL com geração de documento PDF dentro do método `realizar_emprestimo`).
*   **Alto Acoplamento:** O domínio do negócio está rigidamente acoplado à infraestrutura de banco de dados e bibliotecas de terceiros. Isso torna a realização de testes unitários isolados praticamente impossível sem criar um banco real.

**3. Sugestões de Refatoração:**
*   **Separar a persistência:** Criar uma interface `IRepositorio` e classes concretas (`RepositorioLivro`, `RepositorioLeitor`, `RepositorioEmprestimo`) para encapsular todo o acesso ao banco de dados.
*   **Separar serviços externos:** Isolar o envio de e-mails na classe `ServicoNotificacao` e a geração de PDFs na classe `ServicoRelatorio`.
*   **Injeção de dependência:** Passar instâncias dos repositórios e serviços no construtor de `GerenciadorEmprestimo`, permitindo que ele orquestre o processo chamando as interfaces, respeitando SRP e DIP.