Para utilizar o repositório e criar as tabelas:

Instalar poetry no python >=3.11
```bash
pip install poetry
```

Criar venv e instalar dependencias do projeto:
```bash
cd path/to/project/dir
poetry install
```

Definir ambiente de execução python:
```bash
set PYTHONPATH=%cd%
```

Antes de executar o proximo comando, é necessario ajustar as configurações da conexão com o banco em settings.toml e .secrets.toml

Criar database e tabelas:
```bash
poetry run python core/models/db.py
```
Após executar o código, selecione o sgbd que você deseja utilizar para criar as tabelas.


Para popular as tabelas do banco de dados:
```bash
poetry run python core\scripts\populate_db.py
```
Após executar o código, selecione o sgbd que você deseja utilizar para popular as tabelas.


Existem algumas telas com backend implementado. para executa-los, basta utilizar o seguinte comando no cmd:
substitua 'nome_arquivo_tela' pelo nome do arquivo da tela.
```bash
poetry run python core\telas\'nome_arquivo_tela'.py
```
