from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.models.db import (
    LocalAsyncSession,
    Pacientes,
    GeneroEnum,
    LocalSession,
    LocalSessionDuckDB,
)


def registrar_paciente(
    session: Session,
    nome: str,
    data_nascimento: str,
    genero: GeneroEnum,
    endereco: str = None,
    telefone: str = None,
    email: str = None,
):
    paciente = Pacientes(
        nome=nome,
        data_nascimento=data_nascimento,
        genero=genero,
        endereco=endereco,
        telefone=telefone,
        email=email,
    )

    session.add(paciente)
    session.commit()

    return paciente


def consultar_paciente(session: Session, nome: str):
    query = select(Pacientes).where(Pacientes.nome.like(nome))
    result = (session.scalars(query)).all()

    # print(query)
    if not result:
        print("Paciente não encontrado.")
        return None
    print("Paciente encontrado:")
    print("-----------------------------------")
    for r in result:
        print("ID:", r.id)
        print("Nome:", r.nome)
        print("Data de Nascimento:", r.data_nascimento)
        print("Gênero:", r.genero)
        print("Endereço:", r.endereco)
        print("Telefone:", r.telefone)
        print("Email:", r.email)
    return result


def interface(session: Session):
    while True:
        print("Selecione uma opção:")
        print("1 - Registrar paciente")
        print("2 - Consultar paciente")
        print("q - Sair")
        opcao = input("Opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            data_nascimento = input("Data de nascimento: ")
            genero = input("Gênero(MASCULINO, FEMININO): ")
            endereco = input("Endereço: ")
            telefone = input("Telefone: ")
            email = input("Email: ")

            # verifica se o genero é válido, se não for, pede para digitar novamente somente o genero
            while genero not in ["MASCULINO", "FEMININO", "masculino", "feminino"]:
                genero = input("Gênero(MASCULINO, FEMININO): ")

            # formata a data de nascimento para datetime
            data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")

            registrar_paciente(
                session,
                nome=nome,
                data_nascimento=data_nascimento,
                genero=GeneroEnum[genero.upper()],
                endereco=endereco,
                telefone=telefone,
                email=email,
            )
        elif opcao == "2":
            nome = input("Nome: ")
            consultar_paciente(session, nome=nome)
        elif opcao == "q":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    sgbd = ""
    while sgbd not in ["mysql", "duckdb"]:
        sgbd = input("Digite o SGBD para criar o banco e as tabelas(mysql ou duckdb): ")
    if sgbd == "mysql":
        with LocalSession() as session:
            interface(session)
    elif sgbd == "duckdb":
        with LocalSessionDuckDB() as session:
            interface(session)
