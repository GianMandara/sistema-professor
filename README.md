# Project Title

Sistema web desenvolvido em Python utilizando Flask para auxiliar educadores autônomos na gestão de alunos, conteúdos pedagógicos e agenda de aulas individuais.

O sistema foi projetado para ser simples, leve e executável via navegador, permitindo organizar informações acadêmicas e administrativas de forma prática.
## Authors

- [@GianMandara](https://www.github.com/GianMandara)


## Deployment

Executar a aplicação
python app.py
5 - Acessar no navegador
http://127.0.0.1:5000


## Appendix

📊 Dashboard

O painel principal apresenta informações gerais do sistema.

Funcionalidades:

Total de alunos cadastrados

Total de aulas registradas

Navegação rápida entre as áreas do sistema

👨‍🎓 Gestão de Alunos

Permite o gerenciamento completo dos alunos cadastrados.

Funcionalidades:

Cadastro de alunos

Listagem de alunos

Edição de dados

Exclusão de alunos

Dados registrados:

Nome

Email

Telefone

📅 Agenda de Aulas

Responsável pela organização das aulas agendadas.

Funcionalidades:

Agendamento de aulas

Associação de aluno à aula

Associação de conteúdo pedagógico

Registro de data e horário

Edição de aulas

Exclusão de aulas

📖 Cadastro de Conteúdos

Permite cadastrar conteúdos pedagógicos utilizados nas aulas.

Exemplos:

Gramática

Conversação

Algoritmos

Estruturas de Dados

Os conteúdos cadastrados podem ser vinculados às aulas agendadas.

🧰 Tecnologias Utilizadas

Este projeto foi desenvolvido utilizando as seguintes tecnologias:

Python

Flask

SQLite

HTML

CSS

Jinja2

Estrutura do Projeto

sistema-pedagogico
app.py
database
    escola.db
templates
    base.html
    dashboard.html
    alunos.html
    editar_aluno.html
    agenda.html
    editar_aula.html
README.md
