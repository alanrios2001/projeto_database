from sqlalchemy import select, func
from sqlalchemy.orm import Session, joinedload

from core.models.db import Consultas, Pacientes, LocalSession, LocalSessionDuckDB


def buscar_consulta_paciente(session: Session, nome: str):
    query = (
        select(Consultas)
        .join(Pacientes, Consultas.paciente_id == Pacientes.id)
        .options(joinedload(Consultas.paciente), joinedload(Consultas.medico))
        .where(func.lower(Pacientes.nome).like(f"%{nome.lower()}%"))
    )

    # print(query)
    result = (session.scalars(query)).all()

    if not result:
        print("Consulta não encontrada.")
        return None
    print("Consultas encontradas:")
    print("-----------------------------------")
    for r in result:
        print("ID consulta:", r.id)
        print("Data:", r.data)
        print("Paciente:", r.paciente.nome)
        print("Médico:", r.medico.nome)
        print("-----------------------------------")


def interface(session: Session):
    # interface para buscar as consultas de um paciente pelo nome do paciente. sai da interfce ao pressionar q
    while True:
        print('Digite o nome do paciente para buscar as consultas ("q" para sair):')
        nome = input("Nome: ")
        if nome == "q":
            break
        buscar_consulta_paciente(session, nome)


if __name__ == "__main__":
    sgbd = ""
    while sgbd not in ["mysql", "duckdb", "q"]:
        sgbd = input("Digite o SGBD para utilizar na busca do dados(mysql ou duckdb): ")
    if sgbd == "mysql":
        with LocalSession() as session:
            interface(session)
    elif sgbd == "duckdb":
        with LocalSessionDuckDB() as session:
            interface(session)
