# PUC-EngenhariaCloudDevops2026
Projeto da disciplina DevOps (Turma U) da Pós em Engenharia de Serviços e Cloud.

## Descrição
Este projeto apresenta um exemplo simples de aplicação web em Flask, com persistência de dados usando SQLAlchemy e testes automatizados com pytest.

## Bibliotecas usadas
- `flask`
- `flask-sqlalchemy`
- `sqlalchemy`
- `pytest`

## Estrutura básica
- `src/app.py` - aplicação principal Flask
- `src/test_app.py` - testes automatizados
- `src/Entities/book.py` - modelo de entidade de livro
- `instance/templates/` - templates HTML para a interface

## Como executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:
   ```bash
   python src/app.py
   ```
   ```bash
   flask run  
   ```
3. Execute a aplicação com Debug:
   ```bash
   cd /src
   flask run  --debug
   ```

4. Execute os testes:
   ```bash
   pytest
   ```
