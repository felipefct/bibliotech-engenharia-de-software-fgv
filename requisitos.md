# Questão 1: Engenharia de Requisitos

## Requisitos Funcionais

| ID | Descrição | Prioridade |
|----|-----------|------------|
| RF01 | O sistema deve permitir o cadastro de livros informando título, autor, ISBN, categoria e quantidade. | Alta |
| RF02 | O sistema deve permitir o cadastro de leitores com nome, CPF, email e telefone. | Alta |
| RF03 | O sistema deve permitir registrar o empréstimo de um livro para um leitor. | Alta |
| RF04 | O sistema deve calcular automaticamente a data de devolução para 14 dias após o empréstimo. | Alta |
| RF05 | O sistema deve permitir a reserva de um livro caso todos os exemplares estejam emprestados. | Média |
| RF06 | O sistema deve registrar a devolução de livros emprestados. | Alta |
| RF07 | O sistema deve notificar o primeiro leitor da fila de reservas por e-mail quando o livro for devolvido. | Média |
| RF08 | O sistema deve permitir a renovação de um empréstimo por parte do leitor. | Baixa |
| RF09 | O sistema deve calcular multas por atraso na devolução. | Média |
| RF10 | O sistema deve consultar a disponibilidade de exemplares no acervo antes de um empréstimo. | Alta |

## Requisitos Não-Funcionais

| ID | Categoria | Descrição | Métrica |
|----|-----------|-----------|---------|
| RNF01 | Desempenho | O sistema deve processar o registro de um empréstimo rapidamente. | Tempo de resposta < 2 segundos |
| RNF02 | Confiabilidade | O sistema deve garantir que os dados de empréstimos e multas não sejam perdidos. | Backup diário do banco SQLite |
| RNF03 | Interoperabilidade | O sistema deve ser capaz de se integrar com serviços de e-mail. | Uso de protocolo SMTP |
| RNF04 | Usabilidade | O sistema deve ser fácil de usar pelos bibliotecários. | Tempo de treinamento < 2 horas |
| RNF05 | Segurança | O sistema deve proteger os dados pessoais dos leitores cadastrados. | Acesso restrito via autenticação |

## Regras de Negócio

| ID | Descrição |
|----|-----------|
| RN01 | O prazo padrão de empréstimo é fixado em 14 dias a partir da data de registro. |
| RN02 | A multa por atraso na devolução é de R$ 2,00 por dia de atraso. |
| RN03 | Um empréstimo só pode ser renovado se não houver reservas ativas para o livro em questão. |
| RN04 | Um empréstimo só pode ser realizado se houver pelo menos um exemplar disponível no sistema. |
| RN05 | Apenas o primeiro leitor da fila de reservas recebe a notificação inicial quando um livro é devolvido. |

## User Stories

**US01 - Cadastrar Livro**
Como bibliotecário
Quero cadastrar novos livros no sistema
Para manter o acervo da biblioteca atualizado.

Critérios de Aceitação:
- [ ] O sistema deve exigir título, autor, ISBN, categoria e quantidade.
- [ ] Não deve ser possível cadastrar dois livros com o mesmo ISBN.
Story Points: 3

**US02 - Cadastrar Leitor**
Como bibliotecário
Quero registrar o cadastro de novos leitores
Para que eles possam realizar empréstimos.

Critérios de Aceitação:
- [ ] O sistema deve validar se o CPF tem um formato válido.
- [ ] O e-mail deve conter o caractere "@".
Story Points: 2

**US03 - Registrar Empréstimo**
Como bibliotecário
Quero registrar o empréstimo de um livro
Para controlar a saída de exemplares da biblioteca.

Critérios de Aceitação:
- [ ] O sistema deve diminuir a quantidade disponível do livro.
- [ ] O sistema deve gerar o prazo de devolução automaticamente (14 dias).
Story Points: 5

**US04 - Reservar Livro Indisponível**
Como leitor
Quero reservar um livro que está sem exemplares disponíveis
Para garantir que serei o próximo a pegá-lo quando for devolvido.

Critérios de Aceitação:
- [ ] O sistema só permite reserva se os exemplares disponíveis forem 0.
- [ ] O leitor entra no final da fila de reservas daquele livro.
Story Points: 3

**US05 - Notificação de Reserva**
Como sistema
Quero enviar um e-mail para o leitor que reservou um livro
Para avisá-lo que o exemplar foi devolvido e está disponível.

Critérios de Aceitação:
- [ ] O e-mail deve ser enviado via SMTP imediatamente após a devolução.
- [ ] Apenas o primeiro da fila deve ser notificado.
Story Points: 3

**US06 - Aplicar Multa**
Como bibliotecário
Quero que o sistema calcule multas de livros atrasados
Para penalizar adequadamente a não devolução no prazo.

Critérios de Aceitação:
- [ ] O cálculo deve ser automático no momento da devolução.
- [ ] O valor cobrado deve ser de R$ 2,00 por dia.
Story Points: 5