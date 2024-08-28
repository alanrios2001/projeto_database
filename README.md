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

Criar database e tabelas:
```bash
poetry run python models/db.py
```
