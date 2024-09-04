from sqlalchemy import select, update
from sqlalchemy.orm import Session

from core.models.db import Medicamentos, LocalSession, LocalSessionDuckDB


def busca_medicamento(
    session: Session,
    nome: str = None,
    laboratorio: str = None,
):
    query = select(Medicamentos)

    if nome is not None:
        query = query.where(Medicamentos.nome == nome)
    if laboratorio is not None:
        query = query.where(Medicamentos.laboratorio.like(f"%{laboratorio}%"))
    # print(query)
    result = session.scalars(query)

    if result:
        print("Medicamentos encontrados:")
    else:
        print("Nenhum medicamento encontrado.")
        return None
    for row in result:
        print("-----------------------------------")
        print("ID:", row.id)
        print("Nome:", row.nome)
        print("Laboratório:", row.laboratorio)
        print("Quantidade:", row.quantidade)
        print("Validade:", row.validade)

    return result.all()


def retirar_medicamento(session: Session, medicamento_id: int, quantidade: int):
    stmt = (
        update(Medicamentos)
        .where(Medicamentos.id == medicamento_id)
        .values(quantidade=Medicamentos.quantidade - quantidade)
    )
    # print(stmt)
    session.execute(stmt)
    session.commit()


def interface(session: Session):
    # Interface para buscar medicamentos pelo nome e/ou laboratorio e retirar medicamentos q para sair
    # Pode selecionar entre buscar medicamento ou retirar medicamento
    while True:
        print("Selecione uma opção:")
        print("1 - Buscar medicamento")
        print("2 - Retirar medicamento")
        print("q - Sair")
        opcao = input("Opção: ")
        if opcao == "q":
            break
        if opcao == "1":
            nome = input("Digite o nome do medicamento: ")
            laboratorio = input("Digite o laboratório do medicamento: ")
            busca_medicamento(session, nome, laboratorio)
        elif opcao == "2":
            medicamento_id = int(input("Digite o ID do medicamento: "))
            quantidade = int(input("Digite a quantidade a ser retirada: "))
            retirar_medicamento(session, medicamento_id, quantidade)


if __name__ == "__main__":

    sgbd = ""
    while sgbd not in ["mysql", "duckdb", "q"]:
        sgbd = input("Digite o SGBD para criar o banco e as tabelas(mysql ou duckdb): ")
    if sgbd == "mysql":
        with LocalSession() as session:
            interface(session)
    elif sgbd == "duckdb":
        with LocalSessionDuckDB() as session:
            interface(session)
