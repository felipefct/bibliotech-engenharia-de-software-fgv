# Questão 2: Modelagem UML

## a) Diagrama de Classes

```mermaid
classDiagram
    class Bibliotecario {
        +registrarEmprestimo(livro, leitor)
        +registrarDevolucao(emprestimo)
    }

    class Livro {
        -String isbn
        -String titulo
        -String autor
        -String categoria
        -int exemplaresDisponiveis
        +verificarDisponibilidade() bool
        +atualizarEstoque(qtd)
    }
    
    class Exemplar {
        -int numero
        -String status
        +emprestar()
        +devolver()
    }
    
    class Leitor {
        -String cpf
        -String nome
        -String email
        -String telefone
        +cadastrar()
        +consultarHistorico()
    }
    
    class Emprestimo {
        -int id
        -Date dataEmprestimo
        -Date dataDevolucaoPrevista
        -Date dataDevolucao
        +registrar()
        +renovar()
    }

    class Reserva {
        -int id
        -Date dataReserva
        +criarReserva()
        +notificarLeitor()
    }

    class Multa {
        -int id
        -float valor
        -bool paga
        +calcularDiasAtraso()
        +registrarPagamento()
    }
    
    Bibliotecario --> Emprestimo : gerencia
    Livro "1" --> "*" Exemplar : possui
    Emprestimo "*" --> "1" Exemplar : contem
    Emprestimo "*" --> "1" Leitor : pertence a
    Reserva "*" --> "1" Livro : refere-se a
    Reserva "*" --> "1" Leitor : feita por
    Emprestimo "1" --> "0..1" Multa : gera
```

## b) Diagrama de Sequência: Realizar empréstimo de um livro

```mermaid
sequenceDiagram
    actor B as Bibliotecário
    participant S as Sistema
    participant L as Livro
    participant Lei as Leitor
    participant E as Emprestimo

    B->>S: registrarEmprestimo(isbn, cpf)
    S->>L: buscar(isbn)
    L-->>S: dadosLivro
    S->>Lei: buscar(cpf)
    Lei-->>S: dadosLeitor
    S->>L: verificarDisponibilidade()
    
    alt Disponível (exemplares > 0)
        L-->>S: true
        S->>E: novo Emprestimo(isbn, cpf, dataAtual, data+14dias)
        S->>L: atualizarEstoque(-1)
        S-->>B: "Empréstimo realizado com sucesso"
    else Indisponível
        L-->>S: false
        S-->>B: "Livro indisponível. Deseja reservar?"
    end
```

## c) Diagrama de Atividades: Devolver livro e processar reservas

```mermaid
stateDiagram-v2
    [*] --> RegistrarDevolucao: Receber livro do leitor
    
    RegistrarDevolucao --> VerificarAtraso
    
    VerificarAtraso --> CalcularMulta: Data atual > Data Prevista
    VerificarAtraso --> AtualizarEstoque: No prazo (sem multa)
    
    CalcularMulta --> AtualizarEstoque: Salvar multa no BD
    
    AtualizarEstoque --> VerificarReserva: exemplares += 1
    
    VerificarReserva --> NotificarLeitor: Fila de reservas > 0
    VerificarReserva --> FimSemReserva: Sem reservas ativas
    
    NotificarLeitor --> FimComNotificacao: E-mail enviado
    
    FimSemReserva --> [*]
    FimComNotificacao --> [*]
```